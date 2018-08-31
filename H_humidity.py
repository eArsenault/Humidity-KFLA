import numpy as np

def humidex_calc(specific_humidity,pressure,temperature):
    epsilon = 0.62197 # ratio of gas constant of dry air to gas constant of water vapour
    
    vap_pressure = pressure*specific_humidity/(epsilon + (1 - epsilon)*specific_humidity) # Assumes ideal gas. AE Gill, 1982.
    vap_pressure_sat = 6.112*np.exp(17.62*temperature/(243.12 + temperature)) # WMO presentation
    vap_pressure[vap_pressure < 10] = 10 # by def'n of humidex no change is observed if vap_pressure < 10
    
    relative_humidity = vap_pressure/vap_pressure_sat # relative_humidity is to ensure no vap_pressure values are too high
    vap_pressure[relative_humidity > 1] = vap_pressure_sat[relative_humidity > 1] # if vap_pressure would be greater than saturation pressure, set to saturation pressure
    
    dew_point = (1/273.16 - np.log(vap_pressure/6.112)/5417.7530)**(-1) - 273.15 # from Gov. Canada source
    humidex_increase = (0.5555)*(vap_pressure - 10) # from Gov. Canada source
    return temperature + humidex_increase

specific_humidity = np.linspace(0,20)/1000 # divide by 1000 to account for scientific notation in source
pressure = np.linspace(950,1020) 
temperature = np.linspace(15,40)
humidex = humidex_calc(specific_humidity,pressure,temperature)
