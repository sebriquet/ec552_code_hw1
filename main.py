import json
import os
from json_handling import *
from celloapi2 import CelloQuery, CelloResult
from itertools import combinations

# ASK USER TO PROVIDE FILE PATH OF INPUT AND OUTPUT DIRECTORIES AS WELL AS DESIRED GATE
from click._compat import raw_input

prompt = "Please enter the path of your input directory containing: input.json file, output.json file," \
         "UCF.json file and verilog files (boolean gates): "
in_dir = raw_input(prompt)
assert os.path.exists(in_dir), "I did not find directory name at, " + str(in_dir)
prompt2 = "Please enter path for where you want to save results: "
out_dir = input(prompt2)
assert os.path.exists(out_dir), "I did not find directory name at, " + str(out_dir)
v_file = input("Please state which gate (eg: 'and.v') file you want to use: ")
options = 'options.csv'

# define chassis to evaluate
chassis_name = input("which chassis do you want to evaluate: ")
input_sensor_file = f'/{chassis_name}.input.json'
# read input json file
data = open_json(in_dir, input_sensor_file)

# NUMERICAL OPTIMIZATION
# SUBMIT ORIGINAL INPUT FILE
output_device_file = f'{chassis_name}.output.json'
in_ucf = f'{chassis_name}.UCF.json'
# number of inputs into the circuit:
signal_input = 2
# define best circuit score from best 2 input signals (out of the 4 available)
best_score = 0
best_input_signals = None
q = CelloQuery(
    input_directory=in_dir,
    output_directory=out_dir,
    verilog_file=v_file,
    compiler_options=options,
    input_ucf=in_ucf,
    input_sensors=input_sensor_file,
    output_device=output_device_file,
    # logging=True,
)
signals = q.get_input_signals()
signal_pairing = list(combinations(signals, signal_input))
for signal_set in signal_pairing:
    signal_set = list(signal_set)
    q.set_input_signals(signal_set)
    # OBTAIN RESULTS FROM CELLO
    q.get_results()
    # Fetch our Results.
    try:
        res2 = CelloResult(results_dir=out_dir)
        if res2.circuit_score > best_score:
            best_score = res2.circuit_score
            best_input_signals = signal_set
    except:
        pass
    q.reset_input_signals()
print("The score of the original circuit is:")
print(best_score)
print(f'Best input signals: {best_input_signals} ')

# OPTIMIZE CIRCUIT WITH THE BEST INPUT SIGNALS FOUND
# extract parameters from best input signals found
[ymax_one, ymin_one, alpha_one, beta_one, ymax_two, ymin_two, alpha_two, beta_two] = extract_parameters(data, best_input_signals)


# first try DNA engineering operations
# 1) STRONGER/ WEAKER PROMOTER (depending on x value)
def change_promoter(ymax, ymin, x):
    new_ymax = ymax * x
    new_ymin = ymin * x
    return new_ymax, new_ymin


# 2) STRONGER/WEAKER RBS (depending on x value)
def change_rbs(beta, x):
    new_beta = beta / x
    return new_beta


# try powers of 10 for x (to make weaker/stronger promoter and RBS)
x_values = [0.0001, 0.001, 0.01, 0.1, 1, 10, 100, 1000]
# TRY NUMERICAL OPTIMIZATION HERE

# if score doesn't improve significantly, use protein-engineering operations
# 3) STRETCH --> x can be at most 1.5
def stretch(ymax, ymin, x):
    new_ymax = ymax * x
    new_ymin = ymin / x
    return new_ymax, new_ymin


# 4) INCREASE SLOPE --> x can be at most 1.05
def increase_slope(alpha, x):
    new_alpha = alpha * x
    return new_alpha


# 7) DECREASE SLOPE --> x can be at most 1.05
def decrease_slope(alpha, x):
    new_alpha = alpha / x
    return new_alpha


# WRITE AND SAVE MODIFIED INPUT JSON FILE
# call modify_parameters_single_signal for both signals

# convert new file to json and save to input directory
new_input_file = f'new{chassis_name}.input.json'
output_json(data, in_dir, new_input_file)

# Submit modified input file to Cello
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
# set inout signals to be the best two found before
q.set_input_signals(best_input_signals)
q.get_results()
# Fetch our Results.
res = CelloResult(results_dir=out_dir)
print(res.circuit_score)

# print how much the circuit score improved after optimization
delta = res.circuit_score - best_score
print("Circuit improved by", delta)
