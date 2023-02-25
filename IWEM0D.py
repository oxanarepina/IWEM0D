
import pandas as pd
import numpy as np

def elevChange(
        time,
        SLR,
        GIA,
        initial_E,
        initial_MTL,
        tidal_range,
        a_MAR,
        b_MAR,
        a_OAR_mangr,
        b_OAR_mangr,
        c_OAR_mangr,
        a_OAR_saltm,
        b_OAR_saltm,
        c_OAR_saltm,
        a_AC,
        mangr_saltm_threshold,
        out_file=None):
    
    """
    
    Input paramaters:
        
        SIMULATION SETTINGS
        
        time: vector of timesteps for simulation (years)
        SLR: vector of sea level rise at each timestep (m/yr)
        GIA: glacio-isostatic adjustment (mm/yr)
        
        SITE-SPECIFIC CONDITIONS
        
        initial_E: initial surface elevation (m AHD)
        initial_MTL: initial mean tide level (m AHD)
        tidal_range: tidal range (m)
        
        SUB-MODEL PARAMETERS
        
        mangr_saltm_threshold: cross-over elevation from mangrove to saltmarsh 
            (m, relative to z - the relative elevation in the tidal frame)
        
        a_MAR, b_MAR: constants in linear mineral matter accumulation sub-model:
            MAR = a_MAR * z + b_MAR
                
        a_OAR_mangr, b_OAR_mangr, c_OAR_mangr: constants in quadratic mangrove 
            sedimentation model:
            OAR_mangr = (a_OAR_mangr * z**2) + (b_OAR_mangr * z) + c_OAR_mangr
        
        a_OAR_saltm, b_OAR_saltm, c_OAR_saltm: constants in quadratic saltmarsh 
            sedimentation model:
            OAR_saltm = (a_OAR_saltm * z**2) + (b_OAR_saltm * z) + c_OAR_saltm
        
        a_AC: constant in linear autocompaction sub-model:
            AC = a_AC * MAR 
    
        OUTPUTS
        
        out_file: filename to save model results (optional, default None - file
            is not saved).
        
            
    """
    
    # Save parameters that were passed to the function to optionally write out later
    #inputs = pd.DataFrame({'Input' : locals().keys(), 'Value' : locals().values()})
    
    
    # Initialise vectors to store data
    
    E = np.ones(len(time)) * initial_E       # absolute surface elevation (m AHD)
    MTL = np.ones(len(time)) * initial_MTL   # mean tide level (m AHD)
    HAT = np.zeros(len(time))                # highest astronomical tide (m AHD)
    z = np.zeros(len(time))                  # relative elevation in tidal frame (m)
    MAR = np.zeros(len(time))                # inorganic sedimentation (mm/yr)
    OAR_mangr = np.zeros(len(time))          # organic sedimentation from mangroves (mm/yr)
    OAR_saltm = np.zeros(len(time))          # organic sedimentation from saltmarsh (mm/yr)
    mangr_or_saltm = np.zeros(len(time))     # organic sedimentation from relevant vegetation (mm/yr)
    OAR = np.zeros(len(time))                # final organic sedimentation (mm/yr)
    AC = np.zeros(len(time))                 # autocompaction of sediment (mm/yr)
    E_gain = np.zeros(len(time))             # change in surface elevation (mm/yr)

    # Iterate through each timestep
    
    for t in range(len(time)):
        
        # Highest astronomical tide
        HAT[t] = tidal_range/2 + MTL[t]
        
        # Calculate the relative elevation within the tidal frame
        z[t] = (E[t] - MTL[t])/(HAT[t] - MTL[t])
        
        # Calculate the inorganic sedimentation at this elevation
        MAR[t] = (a_MAR * z[t]) + b_MAR
        
        # Calculate autocompaction
        AC[t] = a_AC * MAR[t]
        
        # Calculate organic sedimentation
        OAR_mangr[t] = (a_OAR_mangr * z[t]**2) + (b_OAR_mangr * z[t]) + c_OAR_mangr
        OAR_saltm[t] = (a_OAR_saltm * z[t]**2) + (b_OAR_saltm * z[t]) + c_OAR_saltm
        
        # Calculate which vegetation community is present
        if z[t] < mangr_saltm_threshold:
            mangr_or_saltm[t] = OAR_mangr[t]
        else:
            mangr_or_saltm[t] = OAR_saltm[t]
        
        # Adjust organic sedimentation to exclude negative rates
        if mangr_or_saltm[t] < 0:
            OAR[t] = 0
        else:
            OAR[t] = mangr_or_saltm[t]
        
        # Combine sub-models to calculate net elevation change 
        E_gain[t] = MAR[t] + OAR[t] - AC[t]
        
        # Calculate absolute elevations for the next timestep
        if t < len(time)-1:
        
            E[t+1] = E[t] + E_gain[t]/1000 - GIA/1000   
        
            MTL[t+1] = MTL[t] + SLR[t] 
                    

    # Save as dataframe   
    simul_df = pd.DataFrame({'Time' : time,                                 
                             'SLR' : SLR,                                   
                             'Elevation' : E,                              
                             'MTL' : MTL,
                             'HAT' : HAT,
                             'z' : z, 
                             'MAR' : MAR,
                             'AC' : AC,
                             'MangroveOAR' : OAR_mangr,
                             'SaltmarshOAR' : OAR_saltm,
                             'MangroveOrSaltmarsh' : mangr_or_saltm,
                             'OAR' : OAR,
                             'EGain' : E_gain})
    
    
    # Optionally write the data and parameters to a csv file
    if out_file: 
        simul_df.to_csv(out_file, index=False)
        #inputs.to_csv(out_file.replace(".csv", "_INPUTS.csv"), index=False)
        
        
    return(simul_df)
        
