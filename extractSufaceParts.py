import pandas as pd
import numpy as np

def split_and_save_csv_by_x(csv_file, output_file_prefix):
    # Read the CSV file into a DataFrame
    data = pd.read_csv(csv_file)
    
    # Sort data by the X coordinate
    data_sorted = data.sort_values(by='X')
    
    # Determine the number of parts
    num_parts = 20
    part_size = len(data_sorted) // num_parts

    # Split and save each part
    for i in range(num_parts):
        start_index = i * part_size
        if i < num_parts - 1:
            end_index = (i + 1) * part_size
        else:
            end_index = len(data_sorted)  # Ensure the last part includes any remaining rows
        
        part_data = data_sorted.iloc[start_index:end_index]

        # Save each part to a separate CSV file
        part_output_file = f"{output_file_prefix}_part{i+1}.csv"
        part_data.to_csv(part_output_file, index=False)
        print(f"Data saved to '{part_output_file}'.")

if __name__ == "__main__":
    # Example usage
    csv_file = "coordinate_datad2.csv"  # Replace with your CSV file path
    output_file_prefix = "coordinate_datad2"
    
    split_and_save_csv_by_x(csv_file, output_file_prefix)
