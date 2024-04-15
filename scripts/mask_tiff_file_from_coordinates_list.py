import pandas as pd
import geopandas as gpd
from pyimpute import load_training_vector
import tomllib

def export_dataframe_with_raster_features(
    geojson: str, explanatory_rasters: list[str], 
    columns: list[str], output_file_path: str,occurence_absence_dataframe_path:str, response_field: str = "Presence",  *args, **kwargs
    ):
    """
    Args:
        geojson (str): _description_
        explanatory_rasters (list[str]): _description_
        columns (list[str]): _description_
        output_file_path (str): _description_
        response_field (str, optional): _description_. Defaults to "Presence".
    """
    train_xs, train_y = load_training_vector(geojson, explanatory_rasters, response_field=response_field)
    df = pd.DataFrame(train_xs)
    df.loc[:,response_field] = train_y
    df = df[~df[0].isnull()]
    df.columns = columns
    
    occurence_absence = pd.read_parquet(occurence_absence_dataframe_path)[['Latitude','Longitude']].reset_index(drop=True)
    df = df.merge(occurence_absence.reset_index(), left_index=True, right_index=True)
    df.to_parquet(output_file_path)
    return

if __name__ == '__main__':
    with open("mask_tiff_file_from_coordinates_list.toml", "rb") as f:
        config = tomllib.load(f)
    export_dataframe_with_raster_features(**config)
