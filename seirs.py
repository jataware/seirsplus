#!/usr/bin/env python
# coding: utf-8


from sklearn.metrics import mean_squared_error
from datetime import timedelta
import datetime as dt
import pandas as pd
import numpy as np
import argparse
import math
import json
import os


from models import *
import scipy as scipy
import scipy.integrate


'''

# OREGON RUN

python3 seirs.py -startDate=2020-11-01 -endDate=2020-11-30 -dataFile=ethiopia-history.csv -paramFile=init_ET.json -outfile=ethiopiaPreds.csv


NOLH Reference: NOLHDesigns_v6.xls: Generating nearly orthogonal Latin Hypercube designs
at https://nps.edu/web/seed/software-downloads, Copyright (c) 2009 Susan M. Sanchez 

This library is free software; you can redistribuclear
te it and/or modify it under the terms
of the GNU Lesser General Public License as published by the Free Software Foundation.
'''


################### COMMAND LINE ARGS

parser = argparse.ArgumentParser(description="Get user inputs to run model")

parser.add_argument("-startDate", dest="startDate", type=str, help="YYYY-MM-DD to train model")
parser.add_argument("-endDate", dest="endDate", type=str, help="YYYY-MM-DD to end to train model")
parser.add_argument("-dataFile", dest="dataFile", type=str, help="Historical timeseries data")
parser.add_argument("-paramFile", dest="paramFile", type=str, help="User input parameters")
parser.add_argument("-outfile", dest="outfile", type=str, help="Filename of results file .csv")

args = parser.parse_args()

# Read in params
startDate = args.startDate
endDate = args.endDate
dataFile = args.dataFile
paramFile = args.paramFile
outfile = args.outfile


### Read in initialization values, DOE ranges, and build metamodel
wrkDir = os.getcwd()
with open(f"{wrkDir}/inputs/{paramFile}") as jf:
    init = json.load(jf)


# Pull data from init json:    
geo = init["ISO"]
adminLevel = init["ADMIN"]
 
pointEst = init["Point Estimate"]    
params = init["Range Estimate"]     

# Build DOE df
fn = "sevenNOLH.csv"
df_base = pd.read_csv(f"{wrkDir}/doe/{fn}", sep="\t")
numRuns = df_base.shape[0]-1
df_conv = shape_nolh(df_base, params)
df_runs = buildNOLH(df_base, params, numRuns)

# Read in historical data
df_all_states = pd.read_csv(f"{wrkDir}/data/{dataFile}") 


# Run each model in DOE:
startDate = pd.to_datetime(startDate, format="%Y-%m-%d")
endDate = pd.to_datetime(endDate, format="%Y-%m-%d")
days = (endDate - startDate).days + 1
df_actual = stateData(geo,df_all_states,startDate, endDate)
actualCases = df_actual["actualCases"].iloc[0]
actualFatals = df_actual["actualFatalities"].iloc[0]

all_df = []
cases_MSE = []
fatal_MSE = []

# Point Estimates
INITN = pointEst["initn"]
MU_0 = pointEst["mu_0"]
NU = pointEst["nu"]
XI = pointEst["xi"]
INITI = actualCases
INITF = actualFatals
THETA = pointEst["theta"]

if __name__ == "__main__":
    for i in range(df_runs.shape[0]):

        #DOE params
        SIGMA = 1/df_runs.inv_sigma[i]
        GAMMA = df_runs.gamma[i]
        MU_I = df_runs.mu_i[i]
        R0 = df_runs.r0[i]
        PSI = df_runs.psi[i]

        model = SEIRSModel(initN   = INITN,
                           beta    = GAMMA * R0, 
                           sigma   = SIGMA, 
                           gamma   = GAMMA, 
                           mu_I    = MU_I,
                           mu_0    = MU_0,
                           nu      = NU, 
                           xi      = XI,
                           beta_Q  = GAMMA * R0,
                           sigma_Q = SIGMA, 
                           gamma_Q = GAMMA, 
                           mu_Q    = MU_I,
                           theta_E = THETA, 
                           theta_I = THETA, 
                           psi_E   = PSI, 
                           psi_I   = PSI,
                           initI   = INITI,
                           initE   = INITI,
                           initQ_I = INITI,
                           initQ_E = INITI,
                           initR   = 0,
                           initF   = INITF)

        model.run(T=days)

        # capture model output
       # df = wrapper(model)
        df = wrapper(model, days, startDate, endDate, geo, df_all_states)
        all_df.append(df)

        # Cases MSE:
        cases_MSE.append(casesMSE(df))

        # MSE Fatalities:
        fatal_MSE.append(fatalitiesMSE(df))   

    ###################################################################
    ####  Predict Cases and fatalities using params from Test Run #####
    ###################################################################


    # Add a month to training set date
    startDate = pd.to_datetime(startDate, format="%Y-%m-%d")+pd.DateOffset(months = 1)
    endDate = pd.to_datetime(endDate, format="%Y-%m-%d")+pd.DateOffset(months = 1)
    days = (pd.to_datetime(endDate, format="%Y-%m-%d")-pd.to_datetime(startDate, format="%Y-%m-%d")).days + 1

    # Get actual data if theres is any...
    df_actual = stateData(geo,df_all_states,startDate, endDate)
    actualCases = df_actual["actualCases"].iloc[0]
    actualFatals = df_actual["actualFatalities"].iloc[0]


    # Set params from traiing run with min MSE
    cases_min = cases_MSE.index(min(cases_MSE))
    fatal_min = fatal_MSE.index(min(fatal_MSE))


    # Run it for "fatals" first, then "cases"
    predTypes = ["fatals", "cases"]
    df_sim = pd.DataFrame()

    # Point Estimates
    INITN = pointEst["initn"]
    MU_0 = pointEst["mu_0"]
    NU = pointEst["nu"]
    XI = pointEst["xi"]
    INITI = actualCases
    INITF = actualFatals
    THETA = pointEst["theta"]

    # Get Predictions
    for predType in predTypes:
        
        if predType == "fatals":
            
            SIGMA = 1/df_runs.inv_sigma[fatal_min]
            GAMMA = df_runs.gamma[fatal_min]
            MU_I = df_runs.mu_i[fatal_min]
            R0 = df_runs.r0[fatal_min]
            PSI = df_runs.psi[fatal_min]
            
        else:
            #cases
            SIGMA = 1/df_runs.inv_sigma[cases_min]
            GAMMA = df_runs.gamma[cases_min]
            MU_I = df_runs.mu_i[cases_min]
            R0 = df_runs.r0[cases_min]
            PSI = df_runs.psi[cases_min]
            
        modelPred = SEIRSModel(initN   = INITN,
                               beta    = GAMMA * R0, 
                               sigma   = SIGMA, 
                               gamma   = GAMMA, 
                               mu_I    = MU_I,
                               mu_0    = MU_0,
                               nu      = NU, 
                               xi      = XI,
                               beta_Q  = GAMMA * R0,
                               sigma_Q = SIGMA, 
                               gamma_Q = GAMMA, 
                               mu_Q    = MU_I,
                               theta_E = THETA, 
                               theta_I = THETA, 
                               psi_E   = PSI, 
                               psi_I   = PSI,
                               initI   = actualCases,
                               initE   = actualCases,
                               initQ_I = actualCases,
                               initQ_E = actualCases,
                               initR   = actualCases,
                               initF   = actualFatals)

        modelPred.run(T=days)

        # capture model output
        if predType == "fatals":
            
            df_sim = timeseries_it(modelPred, 'numF', days, startDate)
            df_sim = df_sim.rename(columns={'numI': 'predictedCases', 'numF': 'predictedFatalities'})

        #cases
        else:
            df_I = timeseries_it(modelPred, 'numI', days, startDate)

            # merge and rename columns
            df_sim = df_sim.merge(df_I)
            df_sim = df_sim.rename(columns={'numI': 'predictedCases', 'numF': 'predictedFatalities'})

            df_state = stateData(geo,df_all_states,startDate, endDate).reset_index(drop=True)
            
            if df_sim.shape[0] == df_state.shape[0]:
                flag = "both"
                df_pred = merge_actual(df_state, df_sim)
            
            else:
                flag = "nope"
                df_pred = df_sim

    # Prep for writing csv
    df_pred[adminLevel] = geo

    if flag == "both":
        cols = ['timestamp',adminLevel,'actualCases','predictedCases','actualFatalities','predictedFatalities']

    else:    
        cols = ['timestamp',adminLevel,'predictedCases','predictedFatalities']

    df_pred = df_pred[cols]
    df_pred.to_csv(f"results/{outfile}", index=False)



