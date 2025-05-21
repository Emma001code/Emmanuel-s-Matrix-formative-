# DSA HW01 - Sparse Matrix

This program performs operations on sparse matrices (addition, subtraction, and multiplication) and stores the results in files.

## Features

- Load sparse matrices from files
- Perform matrix operations:
  - Addition
  - Subtraction
  - Multiplication
- Save results to files in a 'results' directory
- Interactive menu system with option to quit

## File Format

Matrix files should be in the following format:

rows=<number_of_rows>
cols=<number_of_columns>
(row, column, value)
(row, column, value)

## How to Use

1. Run the program: `python sparse_matrix.py`
2. Choose an operation:
   - 1: Add matrices
   - 2: Subtract matrices
   - 3: Multiply matrices
   - q: Quit the program
3. Enter paths to the two matrix files when prompted
4. copy the relative path of the samplr input file you want to use
5. Results will be saved in the 'results' directory as well as the result of the previously ran results
6. After each operation, you'll be asked if you want to perform another operation
7. View the generated output from the previously ran code in the Result folder 
## Requirements

- Python 3
- No external dependencies required
- Run with Python3 if you are using ubuntu

## Notes

- The program automatically creates a 'results' directory if it doesn't exist
- Matrix dimensions must be compatible for the chosen operation
- Zero values are not stored in the sparse matrix representation

## Acknowledgement

To Alu for this deeply Insightful project!
