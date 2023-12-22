#Sharma, Shambhawi
#CS480 PA02
#A20459117

import sys
import subprocess
import os

def run_sudoku_solver(mode, filepath):
    # Choose the algorithm based on the provided mode
    if mode == 1:
        print("ALGORITHM: Brute Force Search")
        subprocess.run(['python', 'sudoku_brute_force.py', filepath])
    elif mode == 2:
        print("ALGORITHM: Constraint Satisfaction Problem Backtracking Search")
        subprocess.run(['python', 'sudoku_csp_backtracking.py', filepath])
    elif mode == 3:
        print("ALGORITHM: CSP with forward checking and MRV heuristics")
        subprocess.run(['python', 'sudoku_csp_forward_checking.py', filepath])
    elif mode == 4:
        print("ALGORITHM: Test if the completed puzzle is correct")
        subprocess.run(['python', 'sudoku_solution_valid.py', filepath])
    else:
        print("ERROR. Not enough/too many/illegal input arguments.")

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 3:
        print("ERROR. Not enough/too many/illegal input arguments.")
    else:
        try:
            # Parse the mode and filepath from command-line arguments
            mode = int(sys.argv[1])
            filepath = sys.argv[2]
            
            # Print student information and input file name
            print("Sharma, Shambhawi, A20459117 solution:")
            print("INPUT FILE: " + os.path.basename(filepath))
            
            # Run the Sudoku solver based on the provided mode and filepath
            run_sudoku_solver(mode, filepath)
        except ValueError:
            print("ERROR. Not enough/too many/illegal input arguments.")