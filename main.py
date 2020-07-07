import sys
import sqlalchemy as sq
import pandas as pd
from haversine import haversine, Unit
from sklearn.metrics import pairwise_distances
import numpy as np
from sko.GA import GA_TSP

from utils.functions import generate_map

# Settings
MAX_DISTANCE = 2000 # maximum travel distance

prompt="Enter latitude and longitude separated by comma and a space (leave empty to skip and go with default coordinates): "
inp = input(prompt)
try:
    if inp != "":
        INPUT_LAT, INPUT_LON = [int(x) for x in inp.split(', ')]
    else:
        INPUT_LAT, INPUT_LON = 51.355468, 11.100790
        print(f"No input provided, running with default coordinates: {INPUT_LAT, INPUT_LON}")
except:
    print("Wrong input coordinates.")

starting_point = [INPUT_LAT, INPUT_LON]
coord = ['latitude','longitude']

home = pd.DataFrame(
    {
    'brewery_id':0,
    'brewery_name':'HOME',
    'latitude':INPUT_LAT,
    'longitude':INPUT_LON,
    'beer_type':''
    }, index=[0]
)

# Fetch and join data
engine = sq.create_engine('sqlite:///db/beer.db')
query = f"""
SELECT a.brewery_id, a.name as beer_type, b.name as brewery_name, latitude, longitude
FROM beers a
JOIN breweries b
ON a.brewery_id = b.id
JOIN geocodes c
ON a.brewery_id = c.brewery_id
"""
df = pd.read_sql_query(query, engine)


# Concatenate beer types on brewery level for visualization
df_agg = df.copy()
group = ['brewery_id','brewery_name','latitude','longitude']
df_agg = df_agg.groupby(group)['beer_type'].agg(lambda x: '|'.join(x)).reset_index()

# Calculated distances in KM between coordinates
# Discard places which are too far from starting point
# Filter distance matrix and sort by distance
df_loc = pd.concat([home, df_agg]).reset_index(drop=True)
df_loc['distance'] = df_loc.apply(lambda x: haversine(starting_point, [x['latitude'], x['longitude']]), axis=1)
df_loc = df_loc.sort_values(by='distance')
df_loc = df_loc[df_loc['distance'] < MAX_DISTANCE*0.4]

points_coordinate = df_loc[coord].copy()
distance_matrix = pairwise_distances(
    X=points_coordinate,
    metric=haversine
)
num_points = points_coordinate.shape[0]
# raise exception if total number of points is less than 8:
if num_points < 8:
    raise Exception('Not enough factories in this location. Try a different location.')
num_points = num_points-1 if num_points % 2 == 1 else points_coordinate.shape[0]

# Genetic Algorithm for TSP(Travelling Salesman Problem)
def cal_total_distance(routine):
    '''The objective function. input routine, return total distance.
    cal_total_distance(np.arange(num_points))
    '''
    num_points, = routine.shape
    return sum([distance_matrix[routine[i % num_points], routine[(i + 1) % num_points]] for i in range(num_points)])


np.random.seed(2021)

start = pd.Timestamp.now()

dim = 10 # initial number of breweries from which to start
incr = 5 # increment by this number of breweries
best_distance = 0

# Find out optimal number dims (breweries)
while best_distance < MAX_DISTANCE:

    dim += incr

    ga_tsp = GA_TSP(func=cal_total_distance, n_dim=dim, size_pop=num_points, max_iter=200, prob_mut=0.7)
    best_points, best_distance = ga_tsp.run()

# Retrain final result with more iterations
dim -= 5
ga_tsp = GA_TSP(func=cal_total_distance, n_dim=dim, size_pop=num_points, max_iter=500, prob_mut=0.7)
best_points, best_distance = ga_tsp.run()

# reorder the whole route so that start and end is at HOME (index 0)
ls = list(best_points)
best_points = ls[ls.index(0):] + ls[:ls.index(0)] + [0]
best_points_ = np.concatenate([best_points, [best_points[0]], ])
best_points_coordinate = points_coordinate.values[best_points_, :]

# For each step calculate distance traveled from home
no_factories = df_loc.iloc[best_points,:].shape[0]-2
print(f"Found {no_factories} factories:")
dist_from_home = 0
l = len(best_points)
for k in range(l-1):

    dist_from_home += distance_matrix[best_points[k],best_points[k+1]]
    loc = df_loc.iloc[best_points[k+1],:]
    print(f"-> {loc['brewery_name']} ({loc['brewery_id']}); distance {int(dist_from_home)}km")

print(f"\nTotal distance traveled: {int(dist_from_home)}", "\n")


# Find out total number of unique beers collected from all the breweries
ls = df_loc.iloc[best_points,:]['beer_type'].tolist()
collected_beers = '|'.join(map(str, ls))
coll_uniq_beers = collected_beers.split('|')
coll_uniq_beers = [x for x in np.unique(coll_uniq_beers) if x != '']
print("Total unique beers collected: ", len(coll_uniq_beers))
for beer in coll_uniq_beers:
    print(f"-> {beer}")

print()
generate_map(
    dataframe=df_loc.iloc[best_points,:],
    lat_col='latitude',
    long_col='longitude',
    home=starting_point,
    filename='visited_factories'
    )
print()
print(f"Total runtime: {pd.Timestamp.now()-start}")