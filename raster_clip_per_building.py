import pandas as pd
import geopandas as gpd
import rasterio as rio
import os 
import numpy as np
from shapely.geometry import box
from shapely.geometry import mapping
from rasterio.mask import mask


# Define the directory containing the files
directory = '/put/your/directory'  # replace with your directory path

# List to store filenames
files = []

# Loop through all files in the directory
for filename in os.listdir(directory):
    # Get the full file path
    filepath = os.path.join(directory, filename)
    
    # Check if it is a file (not a directory)
    if os.path.isfile(filepath):
        files.append(filepath)

for file in files:
    file_name = file.split('/')[-1].split('.')[0] + '.tif'
    raster_path = os.path.join('/put/your/directory', file_name)
    gdf = gpd.read_file(file)
    
    # Define the parent directory and the new directory name
    parent_directory = '/put/your/directory'  # replace with your parent directory path
    new_directory_name = file.split('/')[-1].split('.')[0].split('_')[-1]  # replace with your new directory name

    # Combine them to get the full path of the new directory
    new_directory_path = os.path.join(parent_directory, new_directory_name)

    # Create the new directory
    os.makedirs(new_directory_path, exist_ok=True)

    print(f"New directory created at: {new_directory_path}")

    # Open the raster file
    with rio.open(raster_path) as src:
        # Iterate over each row in the GeoDataFrame
        for idx, row in gdf.iterrows():
            f_name = row['building_id']
            output_path = os.path.join(new_directory_path, f"{f_name}.tif")

            if not os.path.exists(output_path):
                
                
                # Buffer the geometry by 600 meters
                buffered_geometry = row['geometry'].buffer(600, cap_style=3)

                # Clip the raster using the buffered geometry
                out_image, out_transform = mask(src, [mapping(buffered_geometry)], crop=True)

                # Update metadata to reflect the new dimensions
                out_meta = src.meta.copy()
                out_meta.update({
                    "driver": "GTiff",
                    "height": out_image.shape[1],
                    "width": out_image.shape[2],
                    "transform": out_transform
                })
                # Define output file path
                output_path = os.path.join(new_directory_path, f"{f_name}.tif")

                # Save the clipped raster to a new file
                with rio.open(output_path, "w", **out_meta) as dest:
                    dest.write(out_image)

                print(f"Saved clipped raster to {output_path}")

            else:
                print('file exists')
