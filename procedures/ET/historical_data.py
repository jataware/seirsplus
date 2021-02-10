#!/usr/bin/env python


from sqlalchemy import create_engine
import pandas as pd
import json
import os


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


fn = f'inputs/model_parameters.json'
with open(f"{fn}") as jf:
    init = json.load(jf)

iso2 = init["ISO"]




