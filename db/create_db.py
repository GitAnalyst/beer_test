from sqlalchemy import create_engine
import pandas as pd
import glob

# Create the db engine
engine = create_engine('sqlite:///db/beer.db')

# Store the dataframes as tables
path = "data\\"
all_files = glob.glob(path + "/*.csv")
li = []
for filename in all_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    tbl_name = filename.replace(path,'').replace('.csv','')
    df.to_sql(tbl_name, engine)