import argparse
import os
import multiprocessing

# Function to check if there is no file
def validate_file_path(file_path):
    if not os.path.exists(file_path):
        raise argparse.ArgumentTypeError(f"'{file_path}' does not exist")
    return file_path

# Function to accept the command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description="Cellular Matrix Simulator")
    # sets the default file to "time_step_0.dat for testing"
    parser.add_argument("-i", "--input", type=validate_file_path, default="time_step_0.dat", help="Path to input file")
    parser.add_argument("-o", "--output", type=str, required=True, help="Path to output file")
    parser.add_argument("-p", "--processes", type=int, default=1, help="Number of processes")
    args = parser.parse_args()
    return args

# Function to read the file
def read_matrix_file(input_file):
    matrix = []
    with open(input_file, 'r') as f:
        for line in f:
            matrix.append(list(line.strip()))
    return matrix

# Function to write the file to output
def write_matrix_file(output_file, matrix):
    with open(output_file, 'w') as f:
        for row in matrix:
            f.write(''.join(row) + '\n')

# Function to count living neighbors of a cell using the dimensions of the matrix
def count_living_neighbors(matrix, row, col):
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    count = 0
    # Define the relitive positions for posible neighbors 
    offsets = [(-1, -1), (-1, 0), (-1, 1),
               (0, -1),           (0, 1),
               (1, -1),  (1, 0),  (1, 1)]
    # Define wrap around for the matrix vertically and horizontally 
    for dr, dc in offsets:
        r = (row + dr) % num_rows  # Wrap around for rows
        c = (col + dc) % num_cols  # Wrap around for columns
        if matrix[r][c] == 'O':    # If neighbor is alive inc count by 1 
            count += 1

    return count

# Function to update cell state based on the rubric rules
def update_cell_state(cell, livingNeighbors):
    if cell == 'O':  # Alive cell
        if is_prime(livingNeighbors): # Check prime
            return 'O'
        else:
            return '.'  # Become dead
    else:
        if livingNeighbors % 2 == 0 and livingNeighbors != 0:
            return 'O'  # Become alive
        else:
            return '.'

# Function to check if a number is prime
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Function to process a chunk of the matrix
def process_chunk(args):
    rowIndex, chunk = args
    processedChunk = []
    for row in chunk:
        processedRow = []
        for colIndex, cell in enumerate(row):
            livingNeighbors = count_living_neighbors(rowIndex, colIndex)
            nextCell = update_cell_state(cell, livingNeighbors)
            processedRow.append(nextCell)
        processedChunk.append(processedRow)
    return processedChunk

# Main function
def main():
    # Parse command-line arguments
    args = parse_arguments()
    input_file = args.input
    output_file = args.output
    num_processes = args.processes

    # Read the initial matrix from the input file
    matrix = read_matrix_file(input_file)

    # Print the project Heading (R#)
    print("Project :: 11734085")

  # Perform 100 generations (starting at 1 means the input-file is counted out)
    for generation in range(1, 101):
      # Update the matrix for the next generation
      matrix = update_matrix(matrix)

      # Print the step and the matrix
      print("\nStep {}\n".format(generation))
      print_matrix(matrix)

    # Write the final matrix to the output file
    write_matrix_file(output_file, matrix)
    print("Matrix after 100 generations written to", output_file)

# Function to print the matrix
def print_matrix(matrix):
    for row in matrix:
        print(''.join(row))

# Function to update the matrix for the next generation
def update_matrix(matrix):
    numRows = len(matrix)
    numCols = len(matrix[0])
    newMatrix = [['.' for _ in range(numCols)] for _ in range(numRows)]

    for i in range(numRows):
        for j in range(numCols):
            livingNeighbors = count_living_neighbors(matrix, i, j)
            # Change matrix from "." to "O"
            newMatrix[i][j] = update_cell_state(matrix[i][j], livingNeighbors)

    return newMatrix

# Main function
if __name__ == "__main__":
    main()
