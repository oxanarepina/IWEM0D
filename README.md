# Model overview

IWEM0D (Intertidal Wetland Evolution Model - 0D) simulates how mangrove forests and saltmarsh wetlands respond to sea-level rise. The model framework, as detailed in Rogers et al. (2023), treats surface elevation change over time as a function of:

- Present elevation `E` 
- Inorganic/mineral matter accumulation rate `MAR`
- Organic matter addition rate `OAR` for mangroves and saltmarsh
- Autocompaction `AC`

Specifically, incremental change in surface elevation `E` over time `t` is modelled as:

`E[t+1] = E[t] + MAR[t] + OAR[t] - AC[t]`

## Sub-models

Mineral deposition `MAR`, organic matter addition `OAR` and autocompaction `AC` are each sub-models that are functions of relative elevation within the tidal frame, `z`:

`z[t] = (E[t] - MTL[t])/(HAT[t] - MTL[t])` 

where:

- `E` is the surface elevation with respect to the Australian Height Datum (AHD; approximately mean sea level)
- `MTL` is the mean tide level, defined with respect to AHD
- `HAT` is the highest astronomical tide, defined with respect to AHD.

The model accounts for sea level rise `SLR` by adjusting the mean tide level at each timestep:

`MTL[t+1] = MTL[t] + SLR[t]`

**Mineral accumulation rate** 

`MAR` is a linear function of `z`, calibrated to have zero accumulation at the highest elevation within the tidal frame:

`MAR[t] = a_MAR * z[t] + b_MAR`

**Organic matter addition rate** 

`OAR` for mangroves and saltmarsh are quadratic functions of `z`:

`OAR_mangr[t] = a_OAR_mangr * z[t]^2 + b_OAR_mangr * z[t] + c_OAR_mangr`

`OAR_saltm[t] = a_OAR_saltm * z[t]^2 + b_OAR_saltm * z[t] + c_OAR_saltm`

**Autocompaction** 

`AC` is a linear function of the amount of mineral accumulation `MAR`, calibrated to have zero autocompaction at the highest elevation within the tidal frame:

`AC[t] = a_AC * MAR[t]`

# Model inputs

## Parameters

For each site, IWEM0D requires the following values to be calibrated:

- The constants `a_MAR` and `b_MAR` in the mineral accumulation sub-model
- The constants `a_OAR_mangr`, `b_OAR_mangr` and `c_OAR_mangr` in the mangrove organic matter addition sub-model
- The constants `a_OAR_saltm`, `b_OAR_saltm` and `c_OAR_saltm` in the saltmarsh organic matter addition sub-model
- The constant `a_AC` in the autocompaction sub-model
- The threshold elevation where mangrove forest transitions to saltmarsh, `mangr_saltm_threshold`.

## Initial conditions

For each site and modelled scenario, IWEM0D requires:

- The initial surface elevation `initial_E` (m AHD)
- The initial mean tide level `initial_MTL` (m AHD)
- The tidal range (m), assumed in Rogers et al. (2023) to remain constant.

## Forcing variables

For each modelled scenario, IWEM0D requires a timeseries of:
- Simulation years
- Sea level rise increments (m/yr).


# Sites and scenarios from Rogers et al. (2023)

The parameters, initial conditions, and sea level rise timeseries used for the simulations in Rogers et al. (2023) are included with this code. These simulations were undertaken for four sites in Westernport Bay, Victoria, Australia:
- French Island
- Kooweerup
- Quail Island
- Rhyll Inlet

For each site, three validation scenarios were run:
- Short-term validation (2000-2020)
- Medium-term validation (1974-2009)
- Long-term validation (0-2009).
