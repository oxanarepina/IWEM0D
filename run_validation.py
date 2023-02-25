"""
Run short-term, medium-term and long-term validation scenarios from Rogers et 
al. (2023) for four sites in Westernport Bay, Victoria.
"""

import os
import pandas as pd
pd.set_option('display.max_columns', None) 

from IWEM0D import elevChange


# %% Read inputs

params = pd.read_csv(r'inputs_validation\Parameters.csv', index_col=0)
initconds = pd.read_csv(r'inputs_validation\InitialConditions.csv', index_col=[0,1,2])

# Set of individual runs to complete 
runs = initconds.index.unique()

# %% Create output directory

out_dir = 'outputs_validation'
if not os.path.isdir(out_dir):
    os.makedirs(out_dir)    


# %% Iterate through scenarios

for run in runs:
    
    site = run[0]
    scenario = run[1]   
    print(run)

    # Read SLR input    
    slr = pd.read_csv(r'inputs_validation\SLR_%s.csv' %(scenario))   
    
    elevChange(
  
      time = slr.Year,
      SLR = slr.SLR, 
      GIA = 0,
      
      initial_E = initconds.loc[run, "initial_E"],
      initial_MTL = initconds.loc[run, "initial_MTL"],
      tidal_range = initconds.loc[run, "tidal_range"],
      
      a_MAR = params.loc[site, "a_MAR"],
      b_MAR = params.loc[site, "b_MAR"],
           
      a_OAR_mangr = params.loc[site, "a_OAR_mangr"],
      b_OAR_mangr = params.loc[site, "b_OAR_mangr"],
      c_OAR_mangr = params.loc[site, "c_OAR_mangr"],
      
      a_OAR_saltm = params.loc[site, "a_OAR_saltm"],
      b_OAR_saltm = params.loc[site, "b_OAR_saltm"],
      c_OAR_saltm = params.loc[site, "c_OAR_saltm"],

      a_AC = params.loc[site, "a_AC"],

      mangr_saltm_threshold = params.loc[site, "mangr_saltm_threshold"],
      
      out_file = os.path.join(out_dir, "_".join(map(str, run))+".csv")
      
      )
    
        
    
