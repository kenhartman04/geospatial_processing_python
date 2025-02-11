from rex import Resource
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import glob

POINTS = [
    ['D', -75.000000000, 36.000000000],
    ['A', -74.000000000, 38.000000000],
    ['B', -74.000000000, 38.000000000],
    ['C', -75.000000000, 36.000000000],
    ['E', -73.000000000, 37.000000000],
    ['F', -74.000000000, 36.000000000]
]

points_df = pd.DataFrame(POINTS, columns=['name', 'latitude', 'longitude'])

# Creating geometry
point_geom = [Point(xy) for xy in zip(points_df.longitude, points_df.latitude)]
points_df = points_df.drop(['longitude', 'latitude'], axis=1)
points_gdf = gpd.GeoDataFrame(points_df, geometry=point_geom, crs=4326).to_crs(32618)

# Paths to WTK, since datasets were not passed through
paths = glob.glob("/your/path/here/*.h5")

# These are columns needed from the actual resource data
inds = points_gdf.sindex.nearest(points_gdf.unary_union)

# Initialize an empty DataFrame to store the combined data
combined_df = pd.DataFrame()

# Taking windspeed, wind direction, and temperature at 160
for f in paths:
    data = Resource(f)
    print(data.meta)
    print(inds.values)
    df_ws = pd.DataFrame(data['windspeed_160m', :, inds.values])
    df_ws.columns = points_df.name + "_ws"
    df_ws.index = data.time_index

    df_wdir = pd.DataFrame(data['winddirection_160m', :, inds.values])
    df_wdir.columns = points_df.name + "_wdir"
    df_wdir.index = data.time_index

    # Concatenate the data for each year
    df_out = pd.concat([df_ws, df_wdir], axis=1)

    # Append to the combined DataFrame
    combined_df = combined_df.append(df_out)

# Save the combined DataFrame to a single CSV file
combined_df.to_csv("/your/path/here/ws_wdir_temp_combined.csv")


# Specify the folder containing the CSV files
folder_path = '/your/path/here/'

# Get a list of all CSV files in the folder
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# Initialize an empty DataFrame to store the combined data
combined_df = pd.DataFrame()

# Loop through each CSV file and append its content to the combined DataFrame
for csv_file in csv_files:
    # Read the CSV file
    file_path = os.path.join(folder_path, csv_file)
    df = pd.read_csv(file_path)

    # Append the DataFrame to the combined DataFrame
    combined_df = pd.concat([combined_df, df], ignore_index=True)
# Save the combined DataFrame to a new CSV file
combined_df.to_csv('/your/path/here/ws_wdir_combined_south.csv', index=False)
