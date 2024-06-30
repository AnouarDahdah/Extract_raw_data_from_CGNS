import pandas as pd
import plotly.express as px

def plot_scatter_from_csv(csv_file, x_col, y_col, z_col, plot_title='Scatter Plot'):
    # Read the CSV file into a DataFrame
    data = pd.read_csv(csv_file)
    
    # Create the scatter plot
    fig = px.scatter(data, x=x_col, y=y_col, color=z_col, title=plot_title, labels={x_col: x_col, y_col: y_col, z_col: z_col})
    
    # Save the plot to an HTML file
    fig.write_html('scatter_plot.html')
    print("Scatter plot saved as 'scatter_plot.html'")

if __name__ == "__main__":
    # Example usage
    csv_file = "/home/adahdah/coordinate_data_part21"  # Replace with your CSV file path
    x_col = 'X'
    y_col = 'Y'
    z_col = 'Z'
    
    plot_scatter_from_csv(csv_file, z_col, x_col, y_col)
