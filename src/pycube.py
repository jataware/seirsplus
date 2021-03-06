import pandas as pd


######## BASELINE FACTORS ##############

d_seven = {'f4': [6, 2, 3, 4, 13, 17, 11, 10, 9, 12, 16, 15, 14, 5, 1, 7, 8],
           'f5': [17, 5, 8, 11, 16, 6, 4, 15, 9, 1, 13, 10, 7, 2, 12, 14, 3],
           'f7': [14, 15, 2, 6, 8, 7, 17, 13, 9, 4, 3, 16, 12, 10, 11, 1, 5],
           'f2': [7, 10, 5, 17, 3, 14, 6, 16, 9, 11, 8, 13, 1, 15, 4, 12, 2],
           'f3': [5, 1, 11, 10, 6, 2, 15, 14, 9, 13, 17, 7, 8, 12, 16, 3, 4],
           'f6': [16, 6, 14, 3, 1, 13, 8, 11, 9, 2, 12, 4, 15, 17, 5, 10, 7],
           'f1': [10, 11, 17, 13, 14, 15, 16, 12, 9, 8, 7, 1, 5, 4, 3, 2, 6]}


d_eleven = {'f1':[33, 30, 29, 19, 31, 32, 23, 18, 22, 25, 24, 26, 20, 28, 21, 27, 17, 1, 4, 5, 15, 3, 2, 11, 16, 12, 9, 10, 8, 14, 6, 13, 7],
            'f2':[4, 33, 15, 29, 2, 31, 16, 23, 9, 22, 8, 24, 6, 20, 7, 21, 17, 30, 1, 19, 5, 32, 3, 18, 11, 25, 12, 26, 10, 28, 14, 27, 13],
            'f3':[15, 5, 30, 33, 16, 11, 32, 31, 8, 10, 25, 22, 7, 13, 28, 20, 17, 19, 29, 4, 1, 18, 23, 2, 3, 26, 24, 9, 12, 27, 21, 6, 14],
            'f5':[7, 13, 6, 14, 8, 10, 9, 12, 18, 23, 32, 31, 19, 29, 30, 33, 17, 27, 21, 28, 20, 26, 24, 25, 22, 16, 11, 2, 3, 15, 5, 4, 1],
            'f6':[29, 16, 2, 31, 23, 15, 1, 30, 24, 8, 12, 25, 20, 6, 13, 27, 17, 5, 18, 32, 3, 11, 19, 33, 4, 10, 26, 22, 9, 14, 28, 21, 7],
            'f8':[21, 7, 20, 6, 24, 8, 22, 9, 11, 18, 3, 32, 5, 19, 1, 30, 17, 13, 27, 14, 28, 10, 26, 12, 25, 23, 16, 31, 2, 29, 15, 33, 4],
            'f11':[23, 25, 24, 27, 14, 6, 13, 8, 1, 4, 5, 16, 32, 31, 22, 19, 17, 11, 9, 10, 7, 20, 28, 21, 26, 33, 30, 29, 18, 2, 3, 12, 15],
            'f4':[16, 11, 2, 3, 19, 29, 30, 33, 7, 13, 6, 14, 26, 24, 25, 22, 17, 18, 23, 32, 31, 15, 5, 4, 1, 27, 21, 28, 20, 8, 10, 9, 12],
            'f9':[33, 30, 11, 15, 3, 2, 29, 18, 20, 28, 13, 8, 12, 9, 24, 27, 17, 1, 4, 23, 19, 31, 32, 5, 16, 14, 6, 21, 26, 22, 25, 10, 7],
            'f7':[23, 15, 32, 4, 5, 18, 1, 31, 20, 7, 21, 6, 10, 26, 12, 25, 17, 11, 19, 2, 30, 29, 16, 33, 3, 14, 27, 13, 28, 24, 8, 22, 9],
            'f10':[20, 28, 13, 8, 23, 25, 10, 7, 3, 2, 22, 19, 1, 5, 30, 18, 17, 14, 6, 21, 26, 11, 9, 24, 27, 31, 32, 12, 15, 33, 29, 4, 16]}

d_sixteen = {'f1':[47, 62, 58, 42, 60, 35, 50, 53, 45, 63, 34, 64, 36, 51, 38, 44, 56, 37, 48, 40, 54, 52, 65, 39, 41, 49, 55, 59, 61, 46, 43, 57, 33, 19, 4, 8, 24, 6, 31, 16, 13, 21, 3, 32, 2, 30, 15, 28, 22, 10, 29, 18, 26, 12, 14, 1, 27, 25, 17, 11, 7, 5, 20, 23, 9],
            'f2':[4, 47, 24, 58, 31, 60, 13, 50, 3, 45, 2, 34, 15, 36, 22, 38, 29, 56, 26, 48, 14, 54, 27, 65, 17, 41, 7, 55, 20, 61, 9, 43, 33, 62, 19, 42, 8, 35, 6, 53, 16, 63, 21, 64, 32, 51, 30, 44, 28, 37, 10, 40, 18, 52, 12, 39, 1, 49, 25, 59, 11, 46, 5, 57, 23],
            'f3':[24, 8, 62, 47, 13, 16, 35, 60, 2, 32, 63, 45, 22, 28, 51, 36, 26, 18, 37, 56, 27, 1, 52, 54, 7, 11, 49, 41, 9, 23, 46, 61, 33, 42, 58, 4, 19, 53, 50, 31, 6, 64, 34, 3, 21, 44, 38, 15, 30, 40, 48, 29, 10, 39, 65, 14, 12, 59, 55, 17, 25, 57, 43, 20, 5],
            'f5':[22, 28, 15, 30, 2, 32, 3, 21, 53, 50, 35, 60, 42, 58, 62, 47, 9, 23, 20, 5, 7, 11, 17, 25, 39, 65, 52, 54, 40, 48, 37, 56, 33, 44, 38, 51, 36, 64, 34, 63, 45, 13, 16, 31, 6, 24, 8, 4, 19, 57, 43, 46, 61, 59, 55, 49, 41, 27, 1, 14, 12, 26, 18, 29, 10],
            'f6':[9, 23, 20, 5, 7, 11, 17, 25, 27, 1, 14, 12, 26, 18, 29, 10, 44, 38, 51, 36, 64, 34, 63, 45, 53, 50, 35, 60, 42, 58, 62, 47, 33, 57, 43, 46, 61, 59, 55, 49, 41, 39, 65, 52, 54, 40, 48, 37, 56, 22, 28, 15, 30, 2, 32, 3, 21, 13, 16, 31, 6, 24, 8, 4, 19],
            'f8':[50, 17, 56, 28, 11, 43, 22, 60, 40, 19, 29, 5, 32, 63, 15, 62, 65, 30, 58, 12, 25, 46, 9, 35, 48, 13, 59, 21, 14, 64, 27, 42, 33, 16, 49, 10, 38, 55, 23, 44, 6, 26, 47, 37, 61, 34, 3, 51, 4, 1, 36, 8, 54, 41, 20, 57, 31, 18, 53, 7, 45, 52, 2, 39, 24],
            'f11':[52, 36, 11, 18, 17, 10, 58, 46, 26, 60, 21, 25, 13, 4, 31, 65, 51, 54, 3, 29, 2, 32, 47, 38, 61, 42, 22, 9, 27, 23, 50, 59, 33, 14, 30, 55, 48, 49, 56, 8, 20, 40, 6, 45, 41, 53, 62, 35, 1, 15, 12, 63, 37, 64, 34, 19, 28, 5, 24, 44, 57, 39, 43, 16, 7],
            'f12':[32, 49, 30, 18, 40, 56, 28, 2, 7, 25, 45, 53, 19, 1, 61, 37, 63, 52, 27, 12, 46, 58, 9, 15, 11, 24, 62, 43, 6, 35, 50, 44, 33, 34, 17, 36, 48, 26, 10, 38, 64, 59, 41, 21, 13, 47, 65, 5, 29, 3, 14, 39, 54, 20, 8, 57, 51, 55, 42, 4, 23, 60, 31, 16, 22],
            'f13':[63, 47, 27, 9, 40, 58, 11, 17, 52, 44, 2, 21, 62, 34, 10, 30, 38, 24, 35, 53, 20, 12, 37, 65, 7, 25, 50, 48, 15, 5, 60, 43, 33, 3, 19, 39, 57, 26, 8, 55, 49, 14, 22, 64, 45, 4, 32, 56, 36, 28, 42, 31, 13, 46, 54, 29, 1, 59, 41, 16, 18, 51, 61, 6, 23],
            'f14':[47, 60, 38, 64, 32, 8, 29, 21, 20, 1, 16, 25, 62, 35, 54, 53, 39, 48, 52, 57, 7, 23, 22, 5, 11, 30, 17, 24, 56, 51, 63, 40, 33, 19, 6, 28, 2, 34, 58, 37, 45, 46, 65, 50, 41, 4, 31, 12, 13, 27, 18, 14, 9, 59, 43, 44, 61, 55, 36, 49, 42, 10, 15, 3, 26],
            'f15':[36, 50, 52, 59, 5, 27, 23, 2, 55, 44, 47, 35, 10, 17, 1, 24, 21, 8, 32, 4, 28, 60, 37, 46, 18, 3, 15, 25, 57, 40, 53, 54, 33, 30, 16, 14, 7, 61, 39, 43, 64, 11, 22, 19, 31, 56, 49, 65, 42, 45, 58, 34, 62, 38, 6, 29, 20, 48, 63, 51, 41, 9, 26, 13, 12],
            'f16':[61, 32, 57, 41, 55, 51, 59, 42, 26, 3, 13, 17, 4, 20, 29, 8, 19, 1, 6, 28, 12, 21, 18, 14, 43, 56, 39, 64, 36, 44, 35, 50, 33, 5, 34, 9, 25, 11, 15, 7, 24, 40, 63, 53, 49, 62, 46, 37, 58, 47, 65, 60, 38, 54, 45, 48, 52, 23, 10, 27, 2, 30, 22, 31, 16],
            'f4':[13, 16, 31, 6, 42, 58, 62, 47, 22, 28, 15, 30, 64, 34, 63, 45, 27, 1, 14, 12, 40, 48, 37, 56, 9, 23, 20, 5, 59, 55, 49, 41, 33, 53, 50, 35, 60, 24, 8, 4, 19, 44, 38, 51, 36, 2, 32, 3, 21, 39, 65, 52, 54, 26, 18, 29, 10, 57, 43, 46, 61, 7, 11, 17, 25],
            'f9':[41, 23, 34, 14, 39, 5, 48, 3, 16, 55, 4, 38, 12, 44, 20, 64, 42, 6, 57, 17, 53, 10, 36, 15, 1, 37, 8, 47, 21, 40, 7, 35, 33, 25, 43, 32, 52, 27, 61, 18, 63, 50, 11, 62, 28, 54, 22, 46, 2, 24, 60, 9, 49, 13, 56, 30, 51, 65, 29, 58, 19, 45, 26, 59, 31],
            'f7':[53, 23, 18, 56, 46, 12, 7, 36, 34, 2, 16, 60, 41, 26, 38, 55, 44, 24, 3, 31, 65, 29, 14, 61, 58, 4, 27, 45, 47, 17, 9, 51, 33, 13, 43, 48, 10, 20, 54, 59, 30, 32, 64, 50, 6, 25, 40, 28, 11, 22, 42, 63, 35, 1, 37, 52, 5, 8, 62, 39, 21, 19, 49, 57, 15],
            'f10':[45, 11, 58, 22, 52, 4, 36, 13, 65, 31, 54, 15, 48, 26, 56, 29, 25, 46, 34, 47, 27, 64, 17, 60, 24, 61, 9, 38, 7, 43, 16, 63, 33, 21, 55, 8, 44, 14, 62, 30, 53, 1, 35, 12, 51, 18, 40, 10, 37, 41, 20, 32, 19, 39, 2, 49, 6, 42, 5, 57, 28, 59, 23, 50, 3]}

####### FUNCTIONS #########
# Choose which base factors to use
def pickBase(numParams):
    
    if numParams <= 16:
        df_base = pd.DataFrame(d_sixteen) 
    if numParams <= 11:
        df_base = pd.DataFrame(d_eleven)     
    if numParams <= 7:
        df_base = pd.DataFrame(d_seven)

    return df_base

# Apply function: transform base factor to user range
def NOLH(x, lo, hi, dc, numRuns):
    return round(lo + ((x-1)*(hi-lo)/numRuns),dc)


# From the base factors, build df and rename columns to user-defined names
def buildNOLH(df, params):
    
    # Resize and rename cols
    dropCol = len(df.columns) - len(params)
    if dropCol > 0:
        df.drop(df.columns[-dropCol:], axis=1, inplace=True)

    #...and rename to column headers to param keys
    names  = pd.DataFrame(params).columns.to_series()
    df.columns = names
    
    # Convert base numbers to user ranges
    numRuns = df.shape[0]-1
    
    df_runs = df.copy(deep=True)

    for key in params.keys():
        lo = params[key][0]
        hi = params[key][1]
        dc = params[key][2]

        df_runs[key] = df_runs[key].apply(lambda x: NOLH(x, lo, hi, dc, numRuns))
        
    return df_runs




