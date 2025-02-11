import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import wind_rose as rose


# Define paths in Eagle:
out_dp = "/put/your/path/"
data_dp = "/put/your/path/ws_wdir_combined_mid_20240225.csv"

def wind_roses(file_path, output_dir, height):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Extract the wind speed and direction columns
    wind_speeds = df.filter(regex='ws$')  # Columns ending with 'ws'
    wind_directions = df.filter(regex='wdir$')  # Columns ending with 'wdir'

    legend_kwargs = {"bbox_to_anchor": (1, 1), "loc": "upper left"}
    
    # Iterate over the columns and create a windrose for each
    for speed_col, dir_col in zip(wind_speeds, wind_directions):
        # Create a new WindRose object
        wind_rose = rose.WindRose()

        # Create the windrose data
        wind_rose.make_wind_rose_from_user_data(wind_directions[dir_col], wind_speeds[speed_col], ws=np.arange(0, 26, 1.))

        # Plot the windrose
        ax = wind_rose.plot_wind_rose(ws_right_edges=np.array([5, 10, 15, 20, 25]), legend_kwargs=legend_kwargs)

        # Add a title
        ax.set_title(f'Wind Rose for area {speed_col[:-3]} at {height}m')

        # Save the plot to the specified directory
        plt.savefig(os.path.join(output_dir, f'wind_rose_{speed_col[:-3]}_{height}m_20240226.png'))

        # Show the plot
        plt.show()
