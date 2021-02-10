from sklearn.metrics import mean_squared_error
from sqlalchemy import create_engine
from datetime import timedelta
import datetime as dt
import pandas as pd
import numpy as np
import argparse
import math
import json
import os


def get_localedb(iso2):
        
    wrkDir = os.getcwd()
    fn = f'inputs/credentials.json'
    with open(f"{fn}") as jf:
        creds = json.load(jf)
        
    pg_usr = creds['username']
    pg_pwd = creds['password']
    pg_host = creds['host']
    pg_port = creds['port']
    pg_db = creds['database']
    engine = create_engine(f'postgresql://{pg_usr}:{pg_pwd}@{pg_host}:{pg_port}/{pg_db}')


    # read in file to convert iso2 to full state name
    state_tx = f"{wrkDir}/data/state_names.txt"
    df_tx = pd.read_csv(state_tx, sep="\t")
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

    
# Block output into 10s because dt=0.1 in models.py script (10 iterations / day) [code lines 130 and 173]
def timeseries_it(model, attr, simDays, startDate):
    
    startDate = pd.to_datetime(startDate, format="%Y-%m-%d")
    
    # get obj attribute of choice
    temp = getattr(model, attr)
    
    #remove starting value and reshape
    temp_ts = []

    temp = temp[1:]
    mat = temp.reshape(simDays, 10)

    # List of averaged number for day
    for i in range(mat.shape[0]):
        temp_ts.append(round(np.average(mat[i]),))

    # create df and add timestamp
    df = pd.DataFrame()
    df[attr]= temp_ts
    
    timestamp = []
    for i in range(simDays):
        tempDate = startDate + timedelta(days=i)
        timestamp.append(tempDate)
    
    df.insert(0, "timestamp", timestamp)

    return df

def stateData(geo,df_all_states,startDate, endDate):
    # Filter to US State of choice (Oregon):
    df_state = df_all_states[df_all_states["state"]==geo].reset_index(drop=True)

    # add timestamp
    df_state.insert(0, "timestamp", df_state.date.apply(lambda x: pd.to_datetime(x, format="%Y-%m-%d")))  
    
    # pare down to needed columns
    df_state = df_state[["timestamp","positive","death"]]
    
    # sort ascending date
    df_state = df_state.sort_values(by='timestamp').reset_index(drop=True)      

    # filter by startDate and (startDate+days)
    endDate = pd.to_datetime(endDate, format="%Y-%m-%d")
    df_state = df_state[(df_state['timestamp'] >= startDate) & (df_state['timestamp'] <= endDate)]

    #rename...
    df_state = df_state.rename(columns={'positive': 'actualCases', 'death': 'actualFatalities'})  
    
    return df_state

def merge_actual(df_state, df_sim):

    #merge actual and simulated timeseries data and get rid of .0
    df = df_state.merge(df_sim)
    df["actualCases"] = df.actualCases.apply(lambda x: round(x,))
    df["actualFatalities"] = df.actualFatalities.apply(lambda x: round(x,))
    
    # reorder columns
    cols = ['timestamp','actualCases','predictedCases','actualFatalities','predictedFatalities']
    df = df[cols]
    
    return df

#def wrapper(model):
def wrapper(model, days, startDate, endDate, geo, df_all_states):
    # Call function for number infected and fatalities
    df_I = timeseries_it(model, 'numI', days, startDate)
    df_F = timeseries_it(model, 'numF', days, startDate)

    # merge and rename columns
    df_sim = df_I.merge(df_F)
    df_sim = df_sim.rename(columns={'numI': 'predictedCases', 'numF': 'predictedFatalities'})

    # Add actual data and format
    df_state = stateData(geo,df_all_states,startDate, endDate)
    df = merge_actual(df_state, df_sim)
    
    return df

def casesMSE(df):
    testCases = df['actualCases']
    predCases = df['predictedCases']
    return mean_squared_error(testCases, predCases)

def fatalitiesMSE(df):
    testF = df['actualFatalities']
    predF = df['predictedFatalities']
    return mean_squared_error(testF, predF)
