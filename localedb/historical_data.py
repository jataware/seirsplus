#!/usr/bin/env python


from sqlalchemy import create_engine
from pathlib import Path
import pandas as pd
import argparse
import json
import os


'''

python3 historical_data.py -username=<username> -password=<pwd> -iso2=ET

'''

wrkDir = os.getcwd()
upDir = str(Path(wrkDir).parents[0])


################### COMMAND LINE ARGS  ###################

parser = argparse.ArgumentParser(description="Get user inputs to run model")

parser.add_argument("-username", dest="username", type=str, help="localedb username")
parser.add_argument("-password", dest="password", type=str, help="localedb password")
parser.add_argument("-iso2", dest="iso2", type=str, help="Two-letter ISO2 code for country or US state abbreviation")
args = parser.parse_args()

# Read in params
pg_usr = args.username
pg_pwd = args.password
iso2 = args.iso2
pg_host = "localhost"
pg_port = 5433
pg_db = "localedb"

# read in file to convert iso2 to full state name
state_tx = f"{wrkDir}/state_names.txt"
df_tx = pd.read_csv(state_tx, sep="\t")


def get_localedb(iso2, engine, df_tx):
     
    state_conv_d = df_tx.set_index("state").to_dict()
    state_list = list(state_conv_d['Name'].keys())   

    # if US state...
    if iso2 in state_list:
        state_conv_d = state_conv_d['Name']
        state = state_conv_d[iso2]

        states = pd.read_sql(f"SELECT * FROM main.locale WHERE admin1='{state}';",engine)
        state_ids = ','.join([str(i) for i in list(states.id)])
        df = pd.read_sql(f"SELECT * FROM dis.dyn WHERE locale_id in ({state_ids});",engine)

        # Rename cols and pare down to what's needed for SEIRS
        df = df.rename(columns={'day': 'date', 'n_conf': 'positive', 'n_dead': 'death'})

        # Collapse on `day` to get counts for the whole State of Oregon
        df = df.groupby(['date']).sum().reset_index()

        df['state'] = iso2
        df = df[['date','state','positive','death']]  

    # if non-US geo
    else:    
        db_id= pd.read_sql(f"SELECT * FROM main.locale WHERE iso2='{iso2}';",engine)['id'].values[0]
        df = pd.read_sql(f"SELECT * FROM dis.dyn WHERE locale_id={db_id};",engine)

        # Rename cols and pare down to what's needed for SEIRS
        df = df.rename(columns={'day': 'date', 'n_conf': 'positive', 'n_dead': 'death'})

        df['state'] = iso2
        df = df[['date','state','positive','death']]  
    
    return df

if __name__ == "__main__":

    try:
        engine = create_engine(f'postgresql://{pg_usr}:{pg_pwd}@{pg_host}:{pg_port}/{pg_db}')
        df_hist = get_localedb(iso2, engine, df_tx)

        fn = f"{upDir}/procedures/{iso2}/inputs/history.csv"
        df_hist.to_csv(fn, index=False)

        print(f"Localedb data for '{iso2}' written to {fn}")
        
    except Exception as e:
        print(f'Failed to upload to data: '+ str(e))   
        print('\n') 
        print("Unable to access historical data via localedb; Ensure that localedb is running locally.")
        print('\n')
