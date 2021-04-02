import json
import os
from random import choice


# file with helper functions to run main script


# function to open and extract data from json file (input)
def open_json(in_dir, file_name):
    input_file = in_dir + file_name
    file = open(input_file, "r")
    data = json.load(file)
    file.close()
    return data


# function to write modified input json file with optimized parameters
def output_json(data, in_dir, new_file_name):
    new_file = json.dumps(data, indent=4)
    complete_name = os.path.join(in_dir, new_file_name)
    f = open(complete_name, "w")
    f.write(new_file)
    f.close()


# function to extract parameters from  best 2 input signals
def extract_parameters(data, best_input_signals):
    if len(best_input_signals) > 2: # checks whether gate is struct.v
        signal_one = choice(best_input_signals)
        signal_two = choice(best_input_signals)
    else:
        signal_one = best_input_signals[0]
        signal_two = best_input_signals[1]
    # check for signal one
    if signal_one == 'LacI':
        parameters_one = data[1].get("parameters")
    elif signal_one == 'TetR':
        parameters_one = data[4].get("parameters")
    elif signal_one == "AraC":
        parameters_one = data[7].get("parameters")
    elif signal_one == 'LuxR':
        parameters_one = data[10].get("parameters")
    # extract ymax, ymin, alpha and beta parameters
    ymax_one = parameters_one[0].get('value')
    ymin_one = parameters_one[1].get('value')
    alpha_one = parameters_one[2].get('value')
    beta_one = parameters_one[3].get('value')
    # check for signal two
    if signal_two == 'LacI':
        parameters_two = data[1].get("parameters")
    elif signal_two == 'TetR':
        parameters_two = data[4].get("parameters")
    elif signal_two == "AraC":
        parameters_two = data[7].get("parameters")
    elif signal_two == 'LuxR':
        parameters_two = data[10].get("parameters")
    # extract ymax, ymin, alpha and beta parameters
    ymax_two = parameters_two[0].get('value')
    ymin_two = parameters_two[1].get('value')
    alpha_two = parameters_two[2].get('value')
    beta_two = parameters_two[3].get('value')
    return ymax_one, ymin_one, alpha_one, beta_one, ymax_two, ymin_two, alpha_two, beta_two


# function to modify parameters
def modify_parameters_single_signal(data, signal_name, new_ymax, new_ymin, new_alpha, new_beta):
    if signal_name == 'LacI':
        data[1]['parameters'][0]['value'] = new_ymax
        data[1]['parameters'][1]['value'] = new_ymin
        data[1]['parameters'][2]['value'] = new_alpha
        data[1]['parameters'][3]['value'] = new_beta
    elif signal_name == 'TetR':
        data[4]['parameters'][0]['value'] = new_ymax
        data[4]['parameters'][1]['value'] = new_ymin
        data[4]['parameters'][2]['value'] = new_alpha
        data[4]['parameters'][3]['value'] = new_beta
    elif signal_name == 'AraC':
        data[7]['parameters'][0]['value'] = new_ymax
        data[7]['parameters'][1]['value'] = new_ymin
        data[7]['parameters'][2]['value'] = new_alpha
        data[7]['parameters'][3]['value'] = new_beta
    elif signal_name == 'LuxR':
        data[10]['parameters'][0]['value'] = new_ymax
        data[10]['parameters'][1]['value'] = new_ymin
        data[10]['parameters'][2]['value'] = new_alpha
        data[10]['parameters'][3]['value'] = new_beta
    return data

