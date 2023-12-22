#Sharma, Shambhawi
#CS480 PA02
#A20459117

import csv
import timeit
import sys

def print_board(board):
    # Function to print the Sudoku board
    for row in board:
        print(",".join(map(str, row)))

def is_valid_mrv(board, row, col, num):
    # Check if placing 'num' at position (row, col) is valid
    for i in range(9):
        if board[row][i] == num or board[i][col] == num:
            return False

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

def get_empty_location_mrv(board):
    # Find the first empty location in the board
    for i in range(9):
        for j in range(9):
            if board[i][j] == 'X':
                return i, j
    return None

def get_domain(board, row, col):
    # Get the domain (possible values) for an empty location
    if board[row][col] != 'X':
        return [board[row][col]]

    domain = list(map(str, range(1, 10)))

    for i in range(9):
        if str(board[row][i]) in domain:
            domain.remove(str(board[row][i]))
        if str(board[i][col]) in domain:
            domain.remove(str(board[i][col]))

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if str(board[start_row + i][start_col + j]) in domain:
                domain.remove(str(board[start_row + i][start_col + j]))

    return domain

def forward_check(board, row, col, num, domain):
    # Perform forward checking after placing 'num' at (row, col)
    for i in range(9):
        if i != col and board[row][i] == 'X' and str(num) in domain[row * 9 + i]:
            domain[row * 9 + i].remove(str(num))

        if i != row and board[i][col] == 'X' and str(num) in domain[i * 9 + col]:
            domain[i * 9 + col].remove(str(num))

    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            r, c = start_row + i, start_col + j
            if (r != row or c != col) and board[r][c] == 'X' and str(num) in domain[r * 9 + c]:
                domain[r * 9 + c].remove(str(num))

def mrv_heuristic(board, domain):
    # Minimum Remaining Values (MRV) heuristic to select the next variable
    min_values = float('inf')
    min_location = None

    for i in range(9):
        for j in range(9):
            if board[i][j] == 'X' and len(domain[i * 9 + j]) < min_values:
                min_values = len(domain[i * 9 + j])
                min_location = (i, j)

    return min_location

def solve_sudoku(board):
    # Main function to solve the Sudoku puzzle using MRV and forward checking
    global node_count
    domain = [get_domain(board, i, j) for i in range(9) for j in range(9)]
    node_count = 0
    start_time = timeit.default_timer()
    result = backtrack(board, domain)
    end_time = timeit.default_timer()
    duration = end_time - start_time
    return result, node_count, duration

def backtrack(board, domain):
    # Recursive backtracking algorithm to solve the Sudoku puzzle
    global node_count
    empty_location = get_empty_location_mrv(board)
    if empty_location is None:
        node_count += 1  # Increment node count when the puzzle is solved
        return True

    row, col = empty_location
    min_location = mrv_heuristic(board, domain)
    if min_location:
        row, col = min_location

    for num in domain[row * 9 + col]:
        if is_valid_mrv(board, row, col, int(num)):
            board[row][col] = int(num)
            node_count += 1
            forward_check(board, row, col, int(num), domain)

            if backtrack(board, domain):
                return True

            board[row][col] = 'X'
            forward_check(board, row, col, int(num), domain)

    return False

def read_csv(file_path):
    # Read the Sudoku puzzle from a CSV file
    with open(file_path, 'r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)
        sudoku_board = [[int(num) if num.isdigit() else 'X' for num in row] for row in reader]
    return sudoku_board

def save_csv(file_path, solution_board):
    # Save the solved Sudoku puzzle to a new CSV file
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(solution_board)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input_file.csv")
        sys.exit(1)

    input_file = sys.argv[1]

    sudoku_board = read_csv(input_file)

    print("Input Puzzle:")
    print_board(sudoku_board)

    solution, node_count, duration = solve_sudoku(sudoku_board)

    if solution:
        print(f"\nNumber of search tree nodes generated: {node_count}")
        print(f"Search Time: {duration:.30e} seconds")
        print("\nSolved Puzzle:")
        print_board(sudoku_board)

        # Save the solution to a new CSV file
        output_file = f"{input_file.split('.')[0]}_SOLUTION.csv"
        save_csv(output_file, sudoku_board)

    else:
        print("\nNo solution found.")