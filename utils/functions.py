### Folium Map
def generate_map(dataframe,lat_col, long_col, home, filename, **kwargs):

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
                           zoom_start=5.5)
        
        # Plot long, lat circles
        for lat, lng, bid, bn, beers in zip(df[lat_col], df[long_col], df['brewery_id'], df['brewery_name'], df['beer_type']):
            folium.CircleMarker(location=[lat, lng],
                          radius=7,
                          fill=True,
                          popup = f"""
                          Location: ({round(lat,3)},{round(lng,3)})
                          Brewery id and name: {bid}, {bn}
                          Available beer types: {beers}""").add_to(mapit)
        folium.PolyLine(locations=df[[lat_col,long_col]]).add_to(mapit)
        folium.Marker(
            location=home,
            icon=folium.Icon(icon='home')
        ).add_to(mapit)

        
        # Save map
        print ('Map completed, saving as {}.html'.format(filename))
        mapit.save('{}.html'.format(filename))
        del df

