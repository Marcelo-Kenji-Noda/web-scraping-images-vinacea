import pandas as pd
from shapely.geometry import Point
import tomllib
import geopandas as gpd
import os

def get_dataframe() -> pd.DataFrame:
    HOME = os.path.dirname(os.path.relpath(__file__))
    with open(os.path.join(HOME,"load_gbif.toml"), "rb") as f:
        config = tomllib.load(f)
    # Ocurrence species data -> OSD_df
    OSD_df = pd.read_parquet(config["input_file_path"])

    # Creating Geometry
    OSD_df['geometry'] = list(zip(OSD_df["Longitude"], OSD_df["Latitude"]))
    OSD_df['geometry'] = OSD_df["geometry"].apply(Point)

    # Create the geodataframe
    OSD_geoframe = gpd.GeoDataFrame(
        OSD_df,
        crs = {'init': 'epsg:4326'},
        geometry = OSD_df['geometry']
    )
    OSD_geoframe = OSD_geoframe.to_crs("EPSG:4326")
    OSD_geoframe.reset_index(drop=True, inplace = True)

    #OSD_geoframe['Year'] = OSD_geoframe['Data'].dt.year
    OSD_df = pd.DataFrame(OSD_geoframe)
    return OSD_df
