import pymatgen.apps.battery.analyzer as ans
import pymatgen.apps.battery.battery_abc as bat
import pymatgen.apps.battery.insertion_battery as ins
import pandas as pd
import numpy as np
import pymatgen
from pymatgen.ext.matproj import MPRester
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import LabelEncoder

MAPI_KEY = 'API'
mpr = MPRester(MAPI_KEY)

def get_battery_data(self, formula_or_batt_id):
    return mpr._make_request('/battery/%s' % formula_or_batt_id)

MPRester.get_battery_data = get_battery_data

def BatteryDF(Ion):
    all_bat_ids_list = (mpr._make_request('/battery/all_ids'))
    all_battery_dataframe = pd.DataFrame([])
    for batt_id in all_bat_ids_list:
        if (batt_id.__contains__(str(Ion))):
            
            result_bat_id = pd.DataFrame(mpr.get_battery_data(batt_id))
            adj_pairs = result_bat_id['adj_pairs']
            adj_pairs_list = list(adj_pairs)
            in_list = pd.DataFrame(list(adj_pairs_list[0]))
            max_d_vol = pd.DataFrame(in_list['max_delta_volume'])
            result_bat_id['Max Delta Volume'] = max_d_vol
            all_battery_dataframe = all_battery_dataframe.append(result_bat_id)

    all_battery_dataframe.rename(columns = {'battid':'Battery ID', 
                                            'reduced_cell_formula':'Reduced Cell Formula', 
                                            'average_voltage':'Average Voltage (V)', 
                                            'min_voltage':'Min Voltage (V)', 
                                            'max_voltage':'Max Voltage (V)', 
                                            'nsteps':'Number of Steps', 
                                            'min_instability':'Min Instability', 
                                            'capacity_grav':'Gravimetric Capacity (units)', 
                                            'capacity_vol':'Volumetric Capacity', 
                                            'working_ion':'Working Ion', 
                                            'min_frac':'Min Fraction', 
                                            'max_frac':'Max Fraction', 
                                            'reduced_cell_composition':'Reduced Cell Composition', 
                                            'framework':'Framework', 
                                            'adj_pairs':'Adjacent Pairs', 
                                            'spacegroup':'Spacegroup', 
                                            'energy_grav':'Gravemetric Energy (units)', 
                                            'energy_vol':'Volumetric Energy', 
                                            'numsites':'Number of Sites', 
                                            'type':'Type'}, inplace = True)
    
    clean_battery_df = all_battery_dataframe.set_index('Battery ID')

df = BatteryDF()

genergye = df['Gravemetric Energy (units)'].values
gcapacity = df['Gravimetric Capacity (units)'].values
callformula =  df['Reduced Cell Formula'].values
voltage = df['Average Voltage (V)'].values
index = df.index

data = {'Grav. Energy':genergye, 'Grav. Capacity':gcapacity, 'Voltage':voltage, 'Formula':callformula, 'Index':index }
new_df = pd.DataFrame(data)
not_unique = len(new_df['Formula'])- len(new_df['Formula'].unique())
print(not_unique)
