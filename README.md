# ec552_code_hw1
Python script for Homework 1 (EC 552: Computational Synthetic Biology for Engineers)

To run the user needs to input the paths for the input directory and the output directory.

Also, the user will be prompted to specify the boolean gate to evaluate as well as the name of the chassis.
The input directory should contain

  - verilog files describing the gates (and.v, nand.v,xor.v, and struct.v)
  - options.csv file
  - input.json file (Eg. Eco1C1G1T1.input.json)
  - output.json file (Eg. Eco1C1G1T1.output.json)
  - UCF.json file  (Eg. Eco1C1G1T1.UCF.json)
  
The scripts saves the CelloResults in the output directory specified.

The script displays the score for the original circuit as well as the score for the optimized circuit.

