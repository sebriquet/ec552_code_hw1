import json
import os
from json_handling import *
from celloapi2 import CelloQuery, CelloResult
from itertools import combinations
from random import seed
from random import random
from random import choice
import matplotlib.pyplot as plt


# ASK USER TO PROVIDE FILE PATH OF INPUT AND OUTPUT DIRECTORIES AS WELL AS DESIRED GATE
from click._compat import raw_input

prompt = "Please enter the path of your input directory containing: \n" \
         " input.json file \n" \
         " output.json file \n" \
         " UCF.json file \n" \
         " and verilog files (boolean gates)  \n" \
         "path: "
in_dir = raw_input(prompt)
assert os.path.exists(in_dir), "I did not find directory name at, " + str(in_dir)
prompt2 = "Please enter path for where you want to save results: "
out_dir = input(prompt2)
assert os.path.exists(out_dir), "I did not find directory name at, " + str(out_dir)
v_file = input("Please state which gate (eg: 'and.v') file you want to use: ")
options = 'options.csv'

# define chassis to evaluate
# chassis_name = input("which chassis do you want to evaluate: ")
chassis_name = 'Eco1C1G1T1'
input_sensor_file = f'/{chassis_name}.input.json'
# read input json file
data = open_json(in_dir, input_sensor_file)

# NUMERICAL OPTIMIZATION
# SUBMIT ORIGINAL INPUT FILE
output_device_file = f'{chassis_name}.output.json'
in_ucf = f'{chassis_name}.UCF.json'
# number of inputs into the circuit:
# check whether gate to test is struct.v
if v_file == 'struct.v':
    signal_input = 3
else:
    signal_input = 2
# define best circuit score from best input signals (out of the 4 available)
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
    new_beta = beta * x
    return new_beta


# generate 4 random numbers between 0.001 and 1000 to DO change RBS and change promoter operations RANDOMLY, to test 100
# circuits with modified input signals and check if score improves
best_score_loop = best_score
seed(12)
scores = []
for i in range(100):
    print(f'Trying input circuit {i} out of 100')
    values = []
    # x = [0.001, 0.01, 0.1, 1, 10, 100, 1000]
    # generate random numbers between 0 and 1
    for n in range(4):
        values.append(random()) # try between 0 and 1
    # modify input values using dna-engineering operations
    [new_ymax_one, new_ymin_one] = change_promoter(ymax_one, ymin_one, choice(values))
    [new_ymax_two, new_ymin_two] = change_promoter(ymax_two, ymin_two, choice(values))
    new_beta_one = change_rbs(beta_one, choice(values))
    new_beta_two = change_rbs(beta_two, choice(values))
    # change this parameters in the data
    data = modify_parameters_single_signal(data, best_input_signals[0], new_ymax_one, new_ymin_one, alpha_one, new_beta_one)
    data = modify_parameters_single_signal(data, best_input_signals[1], new_ymax_two, new_ymin_two, alpha_two, new_beta_two)
    # write these values to new input json file
    new_file = 'loop' + f'{chassis_name}.input.json'
    output_json(data, in_dir, new_file)
    # submit to cello
    m = CelloQuery(
        input_directory=in_dir,
        output_directory=out_dir,
        verilog_file=v_file,
        compiler_options=options,
        input_ucf=in_ucf,
        input_sensors=new_file,
        output_device=output_device_file,
    )
    # set inout signals to be the best two found before
    m.set_input_signals(best_input_signals)
    # get results
    m.get_results()
    # compare if new score is better
    res = CelloResult(results_dir=out_dir)
    # append score of each tested circuit to plot afterwards
    scores.append(res.circuit_score)
    if res.circuit_score > best_score_loop:
        print(f'Improved score: {res.circuit_score}  in comparison to original by delta = {res.circuit_score - best_score}')
        best_score_loop = res.circuit_score
        new_file_optimized = 'best' + f'{chassis_name}.input.json'
        output_json(data, in_dir, new_file_optimized)
    else:
        print("Score did not improve")

# plot results of the simulations
plt.plot(scores)
plt.ylabel("Scores")
plt.xlabel("Circuit number")
plt.title("Scores by randomly changing input parameters")
plt.show()


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


# re-extract parameters from input files with parameters optimized in monte carlo
best_file = '/best' + f'{chassis_name}.input.json'
data2 = open_json(in_dir, best_file)
[ymax_one, ymin_one, alpha_one, beta_one, ymax_two, ymin_two, alpha_two, beta_two] = extract_parameters(data2, best_input_signals)
# do stretch operations in input signal with lowest ymax
if ymax_one < ymax_two:
    [ymax_st, ymin_st] = stretch(ymax_one, ymin_one, 1.5)
    data2 = modify_parameters_single_signal(data2, best_input_signals[0], ymax_st, ymin_st, alpha_one, beta_one)
else:
    [ymax_st, ymin_st] = stretch(ymax_two, ymin_two, 1.5)
    data2 = modify_parameters_single_signal(data2, best_input_signals[1], ymax_st, ymin_st, alpha_two, beta_two)
# convert new file to json and save to input directory
last_input_file = f'new{chassis_name}.input.json'
output_json(data2, in_dir, last_input_file)

# Submit modified input file to Cello
print("Improving score by stretching one of the input signals...")
q = CelloQuery(
   input_directory=in_dir,
   output_directory=out_dir,
   verilog_file=v_file,
   compiler_options=options,
   input_ucf=in_ucf,
   input_sensors=last_input_file,
   output_device=output_device_file,
 )

# Submit our query to Cello. This might take a second.
# set inout signals to be the best two found before
q.set_input_signals(best_input_signals)
q.get_results()
# Fetch our Results.
res3 = CelloResult(results_dir=out_dir)
# print final circuit score and delta value
if res3.circuit_score > best_score_loop:
    print(f"Best score: {res3.circuit_score}")
    print(f"total improvement by delta = {best_score - res3.circuit_score}")
    best_score_loop = res3.circuit_score
else:
    print("Stretch operation did not improve the score!")
    print(f"The best score was: {best_score_loop}")
    print(f"total improvement by delta = {best_score_loop - best_score}")

