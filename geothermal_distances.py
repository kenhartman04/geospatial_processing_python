import geopandas as gpd
from shapely.geometry import Polygon, LineString
import time

start_time = time.time()
# Load the polygon (geothermal plants) and line (roads) data
geothermal_plants_path = '/put/your/directory/here/geothermal_plant_loc_20240604.gpkg'
roads_path_nv = '/put/your/directory/here/roads_here_nv.gpkg'
roads_path_ca = '/put/your/directory/here/roads_here_ca.gpkg'
roads_path_ut = '/put/your/directory/here/roads_here_ut.gpkg'
well_path = '/put/your/directory/here/geothermal_wells_with_well_ids_20240605.gpkg'

geothermal_plants_gdf = gpd.read_file(geothermal_plants_path)
nv_gdf = gpd.read_file(roads_path_nv)
nv_gdf = nv_gdf.dissolve(by='StreetName')
ca_gdf = gpd.read_file(roads_path_ca)
ca_gdf = ca_gdf.dissolve(by='StreetName')
ut_gdf = gpd.read_file(roads_path_ut)
ut_gdf = ut_gdf.dissolve(by='StreetName')
well_gdf = gpd.read_file(well_path)


# create a state column
geothermal_plants_gdf['state'] = 'NV'
geothermal_plants_gdf.loc[geothermal_plants_gdf['plant_id'].isin([25, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114]), 'state'] = 'CA'
geothermal_plants_gdf.loc[geothermal_plants_gdf['plant_id'].isin([29, 30, 31]), 'state'] = 'UT'

#well_gdf['state'] = 'NV'
#well_gdf.loc[well_gdf['plant_id'] == 25, 'state'] = 'CA'
#well_gdf.loc[well_gdf['plant_id'].isin([29, 30, 31]), 'state'] = 'UT'

# Ensure all GeoDataFrames use the same CRS
nv_gdf = nv_gdf.to_crs(geothermal_plants_gdf.crs)
ca_gdf = ca_gdf.to_crs(geothermal_plants_gdf.crs)
ut_gdf = ut_gdf.to_crs(geothermal_plants_gdf.crs)

plant_centroids = geothermal_plants_gdf.geometry.centroid
plant_centroids.geometry.buffer(100)
def calculate_min_distance(plant, state, nv_gdf, ca_gdf, ut_gdf):
    if state == 'NV':
        roads_gdf = nv_gdf
    elif state == 'CA':
        roads_gdf = ca_gdf
    elif state == 'UT':
        roads_gdf = ut_gdf
    else:
        return float('inf')
    
    min_distance = float('inf')
    for road in roads_gdf.geometry:
        distance = plant.distance(road)
        if distance < min_distance:
            min_distance = distance
    return min_distance

# Apply the function to calculate the minimum distance for each plant
geothermal_plants_gdf['min_distance_to_road'] = geothermal_plants_gdf.apply(
    lambda row: calculate_min_distance(row.geometry.centroid, row['state'], nv_gdf, ca_gdf, ut_gdf), axis=1)

# Save the results to a new shapefile
output_path = '/put/your/directory/here/geothermal_plants_with_min_distance_to_roads.gpkg'
geothermal_plants_gdf.to_file(output_path)

print(f"Distances calculated and saved to {output_path}")

# Record the end time
end_time = time.time()
# Calculate the elapsed time
elapsed_time = end_time - start_time
print(f"Elapsed time for the script: {elapsed_time} seconds")

# Save elapsed time to a text file
with open('/put/your/directory/here/elapsed_time.txt', 'w') as file:
    file.write(f"Elapsed time: {elapsed_time} seconds\n")
