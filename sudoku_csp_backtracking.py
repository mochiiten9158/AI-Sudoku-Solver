#Sharma, Shambhawi
#CS480 PA02
#A20459117

import csv
import timeit
import sys

# Global variable to keep track of the number of nodes generated
node_count = 0

# Function to solve the Sudoku puzzle
def solve_sudoku(board):
    global node_count
    node_count = 0

    # Record start time using timeit
    start_time = timeit.default_timer()

    # Call the backtrack function to solve the puzzle
    result = backtrack(board)

    # Record end time using timeit
    end_time = timeit.default_timer()

    # Calculate time taken
    solve_time = end_time - start_time

    # Return the result, number of nodes generated, and time taken
    return result, node_count, solve_time

# Backtracking algorithm to solve the Sudoku puzzle
def backtrack(board):
    global node_count

    # Loop through each cell in the puzzle
    for row in range(9):
        for col in range(9):

            # If the cell is empty (contains 0), try placing numbers 1-9
            if board[row][col] == 0:
                for num in range(1, 10):

                    # Check if placing the number is safe
                    if is_safe(board, row, col, num):
                        board[row][col] = num  # Place the number
                        node_count += 1  # Increment the node count

                        # Recursively call the backtrack function
                        if backtrack(board):
                            return True  # If a solution is found, return True

                        board[row][col] = 0  # If no solution, backtrack

                return False  # If no valid number is found, trigger backtracking

    return True  # If all cells are filled, puzzle is solved

# Function to check if placing a number in a certain position is safe
def is_safe(board, row, col, num):
    return (
        not used_in_row(board, row, num)
        and not used_in_col(board, col, num)
        and not used_in_subgrid(board, row - row % 3, col - col % 3, num)
    )

# Helper function to check if a number is used in the given row
def used_in_row(board, row, num):
    return num in board[row]

# Helper function to check if a number is used in the given column
def used_in_col(board, col, num):
    return num in [board[i][col] for i in range(9)]

# Helper function to check if a number is used in the given subgrid (3x3 block)
def used_in_subgrid(board, start_row, start_col, num):
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return True
    return False

# Function to print the Sudoku puzzle
def print_sudoku(board):
    for row in board:
        # Convert 0s to 'X' for better readability
        row_str = [str(cell) if cell != 0 else 'X' for cell in row]
        print(','.join(row_str))

# Function to save the solution to a CSV file
def save_solution_to_csv(board, input_filename):
    # Create an output filename based on the input filename
    output_filename = input_filename.split('.')[0] + '_SOLUTION.csv'
    
    # Write the solution to the CSV file
    with open(output_filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(board)

# Main function
if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python sudoku_solver.py input_file.csv")
        sys.exit(1)

    # Read input Sudoku puzzle from a CSV file
    input_filename = sys.argv[1]
    with open(input_filename, 'r') as csvfile:
        sudoku_puzzle = [list(map(lambda x: int(x) if x.isdigit() else 0, row)) for row in csv.reader(csvfile)]

    # Display the input Sudoku puzzle
    print("Input Puzzle:")
    print_sudoku(sudoku_puzzle)

    # Apply the Sudoku solver algorithm
    solution, nodes_generated, solve_time = solve_sudoku(sudoku_puzzle)

    # Display the solved Sudoku puzzle or "No solution found"
    if solution:
        # Print additional information
        print(f"\nNumber of search tree nodes generated: {nodes_generated}")
        print(f"Search Time: {solve_time:.30e} seconds")
        print("\nSolved Puzzle:")
        print_sudoku(sudoku_puzzle)
        
        # Save the solution to a CSV file
        save_solution_to_csv(sudoku_puzzle, input_filename)
    else:
        print("\nNo solution found.")