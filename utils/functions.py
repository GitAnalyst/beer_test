### Folium Map
def generate_map(dataframe,lat_col, long_col, home, filename, color_variable=None, **kwargs):

        '''
        Generates a HTML interactive bubble map using folium (mapping library based on Leaflet.js Maps)
        INPUT: df          - pandas dataframe (df)
               lat_col     - latitude column name (str, datatype must be float)
               long_col    - longitude column name (str, datatype must be float)
               home        - list of home coordinates to place a flag
               filename    - path and name of file (str) e.g. 'images/map_name'
               **kwargs    -  Passes options to circle markers:
              ____ Options ____
                radius: (int)
                    The radius of the circle in meters.
                color: (str)
                    The color of the marker's edge in a HTML-compatible format.
                fill: (bool)
                    If true the circle will be filled.
                fill_color: (str) default to the same as color
                    The fill color of the marker in a HTML-compatible format.
                fill_opacity: (float) default 0.2
                    The fill opacity of the marker, between 0. and 1.
                popup: (str), default None (not supported in this function)
                    Input text or visualization for object.
        OUTPUT: None       - Generates HTML interactive map in specified
                             directory infilename
        '''
        import folium
        df = dataframe.copy()
        # Get Map Center
        center_lat = df[lat_col].mean()
        center_long = df[long_col].mean()

        # Generate Map
        mapit = folium.Map(location=[center_lat, center_long],
                           tiles='cartodbpositron',
                           zoom_start=5.25)
        
        if color_variable is not None:
            
            colors = ['#1A5C7F','#E81075', '#E8A02D', '#A9DCD6', '#4A4A4A', '#FFFFFF', '#ECECEC', '#DBDBDB', '#9B9B9B']
            unique_cats = list(df[color_variable].unique())
            cat_colors = dict(zip(unique_cats,colors[:len(unique_cats)]))
            df.loc[:,'colors'] = df[color_variable].map(cat_colors)
        
        else:
            df.loc[:,color_variable] = ['No category provided for coloring']*df.shape[0]
            df.loc[:,'colors'] = ['#1A5C7F']*df.shape[0]

        # Plot long, lat circles
        for lat, lng, color_cat, color in zip(df[lat_col], df[long_col], df[color_variable], df['colors']):
            folium.Circle(location=[lat, lng],
                          radius=50,
                          fill=True,
                          color=color,
                          popup = f'Latitude: {lat}, Longitude: {lng}, Color Category: {color_cat}').add_to(mapit)
        folium.PolyLine(locations=df[[lat_col,long_col]]).add_to(mapit)
        folium.Marker(
            location=home,
            icon=folium.Icon(icon='home')
        ).add_to(mapit)

        
        # Save map
        print ('Map completed, saving as {}.html'.format(filename))
        mapit.save('{}.html'.format(filename))
        del df

def cal_total_distance(routine):
    '''The objective function. input routine, return total distance.
    cal_total_distance(np.arange(num_points))
    '''
    num_points, = routine.shape
    return sum([distance_matrix[routine[i % num_points], routine[(i + 1) % num_points]] for i in range(num_points)])