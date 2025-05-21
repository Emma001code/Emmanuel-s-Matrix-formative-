class SparseMatrix:
    def __init__(self, file_source='', rows=0, cols=0):
        self.non_zero_entries = {} # stores values that are not zero
        self.matrix_rows = rows
        self.matrix_cols = cols

        if file_source:
            self.import_from_file(file_source)
            return

        if rows > 0 and cols > 0:
            self.matrix_rows = rows
            self.matrix_cols = cols

    def import_from_file(self, filepath):
        with open(filepath, 'r') as file:
            #initialise the dimensions
            m_rows, m_cols = file.readline(), file.readline()

            self.matrix_rows = int(m_rows.split('=')[1].strip())
            self.matrix_cols = int(m_cols.split('=')[1].strip())

            # Process each matrix entry
            for l_row in file:
                clean_l_row = l_row.strip()
                if not clean_l_row or not (
                        clean_l_row.startswith('(') and clean_l_row.endswith(')')
                    ):
                    raise SyntaxError('Input file has wrong format')

                try:
                    # Extract data from the entry
                    components = clean_l_row[1:-1].split(',')
                    if len(components) != 3:
                        continue

                    row, col, value = map(int, components)
                    self.set_value(row, col, value)

                except ValueError:
                    # Skip invalid entries
                    continue

    def set_value(self, row, col, value):
        """Set a value in the matrix, removing if zero"""
        if value != 0:
            self.non_zero_entries[(row, col)] = value
        elif (row, col) in self.non_zero_entries:
            del self.non_zero_entries[(row, col)]

    def get_value(self, row, col):
        """Get a value from the matrix, defaulting to 0 if not present"""
        return self.non_zero_entries.get((row, col), 0)

    def sparse_matrix_addition(self, sec_matrix):
        """Add two sparse matrices"""
        if (self.matrix_rows, self.matrix_cols) != (sec_matrix.matrix_rows, sec_matrix.matrix_cols):
            raise ValueError("Matrix dimensions must match for addition")

        new_sparse_matrix = SparseMatrix(rows=self.matrix_rows, cols=self.matrix_cols)

        # Combine all non-zero positions from both matrices
        all_positions = set(self.non_zero_entries.keys()) | set(sec_matrix.non_zero_entries.keys())
        for row, col in all_positions:
            sum_value = self.get_value(row, col) + sec_matrix.get_value(row, col)
            new_sparse_matrix.set_value(row, col, sum_value)

        return new_sparse_matrix

    def sparse_matix_sub(self, sec_matrix):
        """Subtract another matrix from this one"""
        if (self.matrix_rows, self.matrix_cols) != (sec_matrix.matrix_rows, sec_matrix.matrix_cols):
            raise ValueError("Matrix dimensions must match for subtraction")

        new_sparse_matrix = SparseMatrix(rows=self.matrix_rows, cols=self.matrix_cols)

        # Process all positions that might have non-zero differences
        all_positions = set(self.non_zero_entries.keys()) | set(sec_matrix.non_zero_entries.keys())
        for row, col in all_positions:
            diff_value = self.get_value(row, col) - sec_matrix.get_value(row, col)
            new_sparse_matrix.set_value(row, col, diff_value)

        return new_sparse_matrix

    def sparse_matrix_multiplication(self, sec_matrix):
        """Multiply this matrix by another matrix"""
        if self.matrix_cols != sec_matrix.matrix_rows:
            raise ValueError("First matrix columns must match second matrix rows for multiplication")

        new_sparse_matrix = SparseMatrix(rows=self.matrix_rows, cols=sec_matrix.matrix_cols)

        # Organize second matrix entries by row for efficient lookup
        row_entries = {}
        for (row, col), value in sec_matrix.non_zero_entries.items():
            if row not in row_entries:
                row_entries[row] = []
            row_entries[row].append((col, value))

        # Perform the multiplication
        for (row_a, col_a), value_a in self.non_zero_entries.items():
            # Check if this column from matrix A has corresponding rows in matrix B
            if col_a in row_entries:
                # Multiply with all corresponding entries in matrix B
                for col_b, value_b in row_entries[col_a]:
                    current = new_sparse_matrix.get_value(row_a, col_b)
                    new_sparse_matrix.set_value(row_a, col_b, current + (value_a * value_b))

        return new_sparse_matrix

    def export_to_file(self, output_path):
        """Write matrix content to a file"""
        with open(output_path, 'w') as output_file:
            output_file.write(f'rows={self.matrix_rows}\n')
            output_file.write(f'cols={self.matrix_cols}\n')

            for (row, col), value in sorted(self.non_zero_entries.items()):
                output_file.write(f'({row}, {col}, {value})\n')


from os import path, makedirs

def get_operation_choice():
    """Request and validate user operation selection"""
    print("\nAvailable Matrix Operations:")
    print("1. Add Matrices")
    print("2. Subtract Matrices")
    print("3. Multiply Matrices")
    print("q. Quit")

    while True:
        choice = input("\nSelect operation (1-3 or press q to quit): ").strip().lower()
        if choice in {'1', '2', '3', 'q'}:
            return choice
        print("Invalid selection. Please try again.")

def get_continue_choice():
    """Ask user if they want to perform another operation"""
    while True:
        choice = input("\nWould you like to perform another operation? click y for yes and n for No (y/n): ").strip().lower()
        if choice in {'y', 'n'}:
            return choice == 'y'
        print("Invalid input. Please enter 'y' or 'n'.")

def execute_matrix_operations():
    while True:
        # Get user's operation choice
        operation = get_operation_choice()
        if operation == 'q':
            print("\nExiting program. Goodbye dear!")
            return

        # Get input file information
        file_1 = input("Enter path to first matrix file: ").strip()
        file_2 = input("Enter path to second matrix file: ").strip()

        try:
            # Load matrix data
            matrix_one = SparseMatrix(file_source=file_1)
            matrix_two = SparseMatrix(file_source=file_2)

            # Set up output directory
            results_dir = 'results'
            makedirs(results_dir, exist_ok=True)

            # Perform requested operation
            if operation == '1':
                result_matrix = matrix_one.sparse_matrix_addition(matrix_two)
                output_filename = f'{path.basename(file_1).split(".")[0]}_plus_{path.basename(file_2).split(".")[0]}.txt'

            elif operation == '2':
                result_matrix = matrix_one.sparse_matix_sub(matrix_two)
                output_filename = f'{path.basename(file_1).split(".")[0]}_minus_{path.basename(file_2).split(".")[0]}.txt'

            else:  # Multiplication
                result_matrix = matrix_one.sparse_matrix_multiplication(matrix_two)
                output_filename = f'Product_{path.basename(file_1).split(".")[0]}_times_{path.basename(file_2).split(".")[0]}.txt'

            # Save results
            output_path = path.join(results_dir, output_filename)
            result_matrix.export_to_file(output_path)
            print(f"\nOperation completed successfully. Result saved to: {output_path}")

        except ValueError as err:
            print(f"Matrix error: {err}")
        except FileNotFoundError:
            print("Error: Specified file(s) not found.")
        except Exception as err:
            print(f"Operation failed: {err}")

        # Ask if user wants to continue
        if not get_continue_choice():
            print("\nExiting program. Goodbye mydear!")
            return

if __name__ == "__main__":
    print("Sparse Matrix Operations Program")
    print("--------------------------------")
    execute_matrix_operations()
