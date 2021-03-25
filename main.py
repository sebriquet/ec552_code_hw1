import json
import os
from celloapi2 import CelloQuery, CelloResult

# ASK USER TO PROVIDE FILE PATH OF INPUT AND OUTPUT DIRECTORIES AS WELL AS DESIRED GATE
from click._compat import raw_input

prompt = "Plase enter the path of your input directory containing: input.json file, output.json file," \
         "UCF.json file and verilog files (boolean gates): "
in_dir = raw_input(prompt)
assert os.path.exists(in_dir), "I did not find directory name at, " +str(in_dir)
prompt2 = "Please enter path for where you want to save results: "
out_dir = input(prompt2)
assert os.path.exists(out_dir), "I did not find directory name at, " +str(out_dir)
v_file = input("Please state which gate (eg: 'and.v') file you want to use: ")
options = 'options.csv'

#define chassis to evaluate
chassis_name = input("which chassis do you want to evaluate: ")
# read input json file
input_file = in_dir + f'/{chassis_name}.input.json'
file = open(input_file,)
# load json file as a list
data = json.load(file)
#check the data structure loaded correctly
#print(data)
#close file
file.close()

#split list
# LacI
LacI_parameters = data[1].get("parameters")
ymax_lac = LacI_parameters[0].get('value')
ymin_lac = LacI_parameters[1].get('value')
alpha_lac = LacI_parameters[2].get('value')
beta_lac = LacI_parameters[3].get('value')

# TetR
TetR_parameters = data[4].get("parameters")
ymax_tet = TetR_parameters[0].get('value')
ymin_tet = TetR_parameters[1].get('value')
alpha_tet = TetR_parameters[2].get('value')
beta_tet = TetR_parameters[3].get('value')

# AraC
AraC_parameters = data[7].get("parameters")
ymax_ara = AraC_parameters[0].get('value')
ymin_ara = AraC_parameters[1].get('value')
alpha_ara = AraC_parameters[2].get('value')
beta_ara = AraC_parameters[3].get('value')

# LuxR
LuxR_parameters = data[10].get("parameters")
ymax_lux = LuxR_parameters[0].get('value')
ymin_lux = LuxR_parameters[1].get('value')
alpha_lux = LuxR_parameters[2].get('value')
beta_lux = LuxR_parameters[3].get('value')

# NUMERICAL OPTIMIZATION
#intialize parameters for now (there should really be the results from optimization algorithm)
# LacI
new_ymax_lac = 0.1
new_ymin_lac = 0.1
new_alpha_lac = 0.1
new_beta_lac = 0.1
#TetR
new_ymax_tet = 0.1
new_ymin_tet = 0.1
new_alpha_tet = 0.1
new_beta_tet = 0.1
# AraC
new_ymax_ara = 0.1
new_ymin_ara = 0.1
new_alpha_ara = 0.1
new_beta_ara = 0.1
# LuxR
new_ymax_lux = 0.1
new_ymin_lux = 0.1
new_alpha_lux = 0.1
new_beta_lux = 0.1

# WRITE AND SAVE MODIFIED INPUT JSON FILE
#new_file = data
# Lac I
data[1]['parameters'][0]['value'] = new_ymax_lac
data[1]['parameters'][1]['value'] = new_ymin_lac
data[1]['parameters'][2]['value'] = new_alpha_lac
data[1]['parameters'][3]['value'] = new_beta_lac
# Tet R
data[4]['parameters'][0]['value'] = new_ymax_tet
data[4]['parameters'][1]['value'] = new_ymin_tet
data[4]['parameters'][2]['value'] = new_alpha_tet
data[4]['parameters'][3]['value'] = new_beta_tet
# Ara C
data[7]['parameters'][0]['value'] = new_ymax_ara
data[7]['parameters'][1]['value'] = new_ymin_ara
data[7]['parameters'][2]['value'] = new_alpha_ara
data[7]['parameters'][3]['value'] = new_beta_ara
# Lux R
data[10]['parameters'][0]['value'] = new_ymax_lux
data[10]['parameters'][1]['value'] = new_ymin_lux
data[10]['parameters'][2]['value'] = new_alpha_lux
data[10]['parameters'][3]['value'] = new_beta_lux

#covert file to json
new_file = json.dumps(data, indent= 4)
# save file to directory
output_sensor_file = f'new{chassis_name}.input.json'
#add the file to the input directory specified by the user
completeName = os.path.join(in_dir, output_sensor_file)
f = open(completeName, 'w')
#write content
f.write(new_file)
#close file
f.close()

#SUBMIT ORIGINAL INPUT FILE
output_device_file = f'{chassis_name}.output.json'
input_sensor_file = f'{chassis_name}.input.json'
in_ucf = f'{chassis_name}.UCF.json'
q = CelloQuery(
    input_directory=in_dir,
    output_directory=out_dir,
    verilog_file=v_file,
    compiler_options=options,
    input_ucf=in_ucf,
    input_sensors=input_sensor_file,
    output_device=output_device_file,
)
#OBTAIN RESULTS FROM CELLO
# Submit our query to Cello. This might take a second.
q.get_results()
# Fetch our Results.
res2 = CelloResult(results_dir=out_dir)
print("The score of the original circuit is:")
print(res2.circuit_score)

# SUBMIT MODIFIED INPUT FILE TO CELLO
# Set up input files.
in_ucf = f'{chassis_name}.UCF.json'
input_sensor_file = f'new{chassis_name}.input.json'
output_device_file = f'{chassis_name}.output.json'
q = CelloQuery(
    input_directory=in_dir,
    output_directory=out_dir,
    verilog_file=v_file,
    compiler_options=options,
    input_ucf=in_ucf,
    input_sensors=input_sensor_file,
    output_device=output_device_file,
)

# Submit our query to Cello. This might take a second.
q.get_results()
# Fetch our Results.
res = CelloResult(results_dir=out_dir)
print(res.circuit_score)

delta = res.circuit_score - res2.circuit_score
print("Circuit improved by", delta)