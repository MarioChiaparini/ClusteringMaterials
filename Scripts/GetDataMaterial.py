import pymatgen
from pymatgen.ext.matproj import MPRester
#from mp_api.client import MPRester
import os 


Cif = os.path.join('')
API = MPRester(api_key='P5KlMfFhCfKvXJBjNRq')

# Working with sodium section
# Create a query
#battery_Matt = API.summary.search(criteria={"elements": {"$in": ["Na"]}}, properties=["material_id"])

#for material in battery_Matt:
#        material_id = material["material_id"]
#        structure = API.get_structure_by_material_id(material_id)
#        print(f"Output =  {structure}")

get_battery_id = API._make_request('/battery/all_ids') 
print(f"Battery Id: {get_battery_id}")
criteria = {
	'elements':{'$in':get_battery_id}, 
	'elements':{'$in':["Na"]}
}
props = ['material_id', 'formula', 'density', 'band_gap', 'energy_density', 'specific_capacity', 'voltage']
with API as data:
	#docs = data.query( material_ids=['mp-753211', 'mp-755288'])
	battery_materials = data.query(criteria=criteria, properties=props)


if not battery_materials:
	print("No results")
else:
	for material in battery_materials:
		print(f"Material ID: {material['material_id']}")
		print(f"Formula : {material['formula']}")
		#print(f"Oxide Type: {material['oxide_type']}")
		#print(f"Formation Energy: {material['formation_energy_per_atom']}")
		print(f"Band Gap: {material['band_gap']}")
		print(f"Density: {material['density']}")
		print(f"Energy Density: {material['energy_density']}")
		print(f"Specific Capacity: {material['specific_capacity']}")
		print(f"Voltage: {material['voltage']}")
		print("\n")		
