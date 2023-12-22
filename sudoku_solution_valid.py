#Sharma, Shambhawi
#CS480 PA02
#A20459117

import sys
import csv

def is_valid_sudoku_check(board):
    # Check rows and columns
    for i in range(9):
        # Check each row and column using the is_valid_group function
        if not is_valid_group(board[i]) or not is_valid_group([board[j][i] for j in range(9)]):
            return False

    # Check 3x3 squares
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            # Extract a 3x3 square and check it using the is_valid_group function
            square = [board[x][y] for x in range(i, i + 3) for y in range(j, j + 3)]
            if not is_valid_group(square):
                return False

    return True

def is_valid_group(group):
    # Filter out 'X' and check if the length of the set of numbers is the same as the length of the list
    group = [x for x in group if x != 'X']
    return len(set(group)) == len(group)

def read_sudoku_from_file(file_path):
    sudoku_board = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Convert each cell to an integer if it is not 'X', otherwise keep it as 'X'
            sudoku_board.append([int(cell) if cell != 'X' else 'X' for cell in row])
    return sudoku_board

def print_sudoku(board):
    # Print the Sudoku board
    for row in board:
        print(' '.join(map(str, row)))

def check_sudoku(file_path):
    # Read Sudoku from the file
    sudoku_board = read_sudoku_from_file(file_path)

    print("\nInput Puzzle:")
    # Print the input Sudoku puzzle
    print_sudoku(sudoku_board)

    # Check if the Sudoku puzzle is valid using the is_valid_sudoku_check function
    if is_valid_sudoku_check(sudoku_board):
        print("\nThis is a valid, solved, Sudoku puzzle.")
    else:
        print("\nERROR: This is NOT a solved Sudoku puzzle.")

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        print("Usage: python sudoku_check.py <file_path>")
        sys.exit(1)

    # Get the file path from the command-line argument and check the Sudoku puzzle
    file_path = sys.argv[1]
    check_sudoku(file_path)