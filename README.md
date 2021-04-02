# Circuit Optimization using Cello and MonteCarlo 
Python script for Homework 1 (EC 552: Computational Synthetic Biology for Engineers)

To run the user needs to input the paths for the input directory and the output directory.
The ouput directory needs to exist (created beforehand) but it may be empty.

Also, the user will be prompted to specify the boolean gate to evaluate. 
The script will automatically evaluate the Eco1C1G1T1 chassis.

The input directory should contain:

  - verilog files describing the gates (and.v, nand.v,xor.v, and struct.v)
  - options.csv file
  - input.json file (Eg. Eco1C1G1T1.input.json)
  - output.json file (Eg. Eco1C1G1T1.output.json)
  - UCF.json file  (Eg. Eco1C1G1T1.UCF.json)

Files cannot be nested within the input directory.
  
The scripts saves the CelloResults in the output directory specified.
Program saves the modified input.json file with the optimized parameters corresponding to the circuit with the best score in the input directory.

The optimization approach consists of random changes between 0 and 1 to the input signals using DNA-Engineering operations. Testing a total of 100 circuits, a plot depicting the score of each circuit will be created.

Lastly,the script displays the score for the original circuit witht the best two input signals as well as the score for the optimized circuit (using previous signals) and the delta value.

NOTE: The running time is ~2-3 hours depending on the booleat gate to be evualuated (struct.v takes longer).

## Compiling and Running the Code:

To run the script, please follow the instructions for the installation of CelloAPI2.
Once you have cello installed and running on your compueter, you can simply run the command:
  - python3 main.py
  
A folder containing all required input files has been provided under "input".
Plase be careful when prompt to provide the path for the input and output directory as it is case sensitive.

NOTE: The code was tested on MacOS Catalina Version: 10.15.7, using Python 3.9.2

Sample Run:
<img width="727" alt="Screen Shot 2021-04-02 at 5 13 50 PM" src="https://user-images.githubusercontent.com/57968955/113454735-e3427580-93d6-11eb-8521-f33dfcfd1f56.png">

