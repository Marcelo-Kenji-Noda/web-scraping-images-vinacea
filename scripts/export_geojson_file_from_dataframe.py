import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import tomllib

def export_geojson_file_from_dataframe(
    occurence_absence_file_path: str,
    geojson_output_file_path: str
) -> None:
    """
    Args:
        occurence_absence_file_path (str): _description_
        geojson_output_file_path (str): _description_
    """
    coordinates = pd.read_parquet(occurence_absence_file_path)
    coordinates['geometry'] = list(zip(coordinates["Longitude"], coordinates["Latitude"]))
    coordinates = coordinates[['Presence','geometry']].copy()
    coordinates['geometry'] = coordinates["geometry"].apply(Point)
    geo_dataframe = gpd.GeoDataFrame(coordinates)

    # Create the geodataframe
    output_dataframe = gpd.GeoDataFrame(
        geo_dataframe,
        crs = {'init': 'epsg:4326'},
        geometry = geo_dataframe['geometry']
    )
    output_dataframe = output_dataframe.to_crs("EPSG:4326").reset_index(drop=True)
    output_dataframe.to_file(geojson_output_file_path, driver="GeoJSON")
    
    print(f"EXPORT SUCCESS >==> {geojson_output_file_path}")
    return

def main(occurence_absence_file_path: str, geojson_output_file_path:str):  
    export_geojson_file_from_dataframe(
        occurence_absence_file_path=occurence_absence_file_path,
        geojson_output_file_path = geojson_output_file_path
    )

if __name__ == '__main__':
    with open("export_geojson_file_from_dataframe.toml", "rb") as f:
        config = tomllib.load(f)
    main(**config)