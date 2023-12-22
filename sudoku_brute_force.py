#Sharma, Shambhawi
#CS480 PA02
#A20459117

import timeit
import csv
import sys
import codecs

class SudokuSolver:
    def __init__(self, puzzle):
        # Initialize the SudokuSolver with the given puzzle
        self.puzzle = puzzle
        self.valid_set = set(map(str, range(1, 10)))  # Valid numbers in Sudoku
        self.nodes_generated = 0

    def find_empty_location(self):
        # Find the first empty location (cell with 0) in the puzzle
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] == 0:
                    return i, j
        return None

    def is_valid(self, row, col, num):
        # Check if 'num' is not present in the row, column, and the 3x3 grid
        return (
            all(num != self.puzzle[row][j] for j in range(9)) and
            all(num != self.puzzle[i][col] for i in range(9)) and
            all(
                num != self.puzzle[i][j]
                for i in range(row - row % 3, row - row % 3 + 3)
                for j in range(col - col % 3, col - col % 3 + 3)
            )
        )

    def generate_domain(self, row, col):
        # Generate the domain of possible values for a given cell
        if self.puzzle[row][col] != 0:
            return [self.puzzle[row][col]]
        else:
            return list(map(int, self.valid_set))

    def solve_brute_force(self):
        # Recursive solver using brute-force approach
        def recursive_solver():
            find = self.find_empty_location()
            if not find:
                return True
            row, col = find

            domain = self.generate_domain(row, col)

            for num in domain:
                self.nodes_generated += 1
                if self.is_valid(row, col, num):
                    self.puzzle[row][col] = num
                    if recursive_solver():
                        return True
                    self.puzzle[row][col] = 0

            return False

        self.nodes_generated = 0
        if recursive_solver():
            return True
        return False

    def solve(self, input_filename):
        # Solve the Sudoku puzzle using brute-force search
        print("Input Puzzle:")
        self.print_solution()

        # Using timeit to measure execution time
        start_time = timeit.default_timer()
        solved = self.solve_brute_force()
        end_time = timeit.default_timer()

        if solved:
            print(f"\nNumber of search tree nodes generated: {self.nodes_generated}")
            print(f"Search Time: {end_time - start_time:.30e} seconds.")
            print("\nSolved Puzzle: ")
            self.print_solution()
            self.save_solution_to_csv(input_filename)
        else:
            print("\nNo solution found.")

    def print_solution(self):
        # Print the current state of the puzzle
        for row in self.puzzle:
            print(",".join(str(num) if num != 0 else "X" for num in row))

    def save_solution_to_csv(self, input_filename):
        # Save the solved puzzle to a CSV file
        output_filename = f"{input_filename.split('.')[0]}_SOLUTION.csv"

        with open(output_filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            for row in self.puzzle:
                csvwriter.writerow([str(num) if num != 0 else "X" for num in row])

def load_puzzle_from_csv(filename):
    # Load a Sudoku puzzle from a CSV file
    puzzle = []
    with codecs.open(filename, 'r', encoding='utf-8-sig') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            puzzle.append([int(num) if num != 'X' else 0 for num in row])
    return puzzle

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py input_file.csv")
        sys.exit(1)

    input_filename = sys.argv[1]
    input_puzzle = load_puzzle_from_csv(input_filename)

    solver = SudokuSolver(input_puzzle)
    solver.solve(input_filename)  # Using brute force search