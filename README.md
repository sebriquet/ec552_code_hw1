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

NOTE: The running time is ~2 hours.
