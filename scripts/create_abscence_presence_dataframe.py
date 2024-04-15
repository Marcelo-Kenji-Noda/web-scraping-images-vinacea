import geopandas as gpd
import numpy as np
import pandas as pd

import tomllib

def create_dataframe_with_random_points_inside_geom(
    region_dataframe: gpd.GeoDataFrame,
    n_points: int = 100,
    seed: int | None = 42
) -> pd.DataFrame:
    """

    Args:
        region_dataframe (gpd.GeoDataFrame): Geopandas Dataframe with the domain
        n_points (int, optional): Number of random points generated. Defaults to 100.
        seed (int | None, optional): Random seed. Defaults to 42.

    Returns:
        pd.DataFrame: dataframe with columns "Latitude" and "Longitude"
    """
    data = {'geometry': [region_dataframe['geometry'].unary_union]}
    gdf_union = gpd.GeoDataFrame(data, geometry='geometry')
    random_points = gdf_union.sample_points(n_points, rng=seed).explode(index_parts=False)
    coordinates = random_points.apply(lambda point: pd.Series({'Latitude': point.y, 'Longitude': point.x}))
    return pd.DataFrame(coordinates).reset_index(drop=True)


def main(
    occurence_file_path: str,
    states_filter: list[str],
    n_points_per_state: int=250,
    random_seed: int = 42,
    geoshape_filepath: str = "assets/FEATURES/MALHAS/BR_UF_2022.shp",
    output_filepath: str ="assets/INPUT/occurence.parquet",
    state_column_name: str = "SIGLA_UF"
) -> None:
    """
    Args:
        occurence_file_path (str): _description_
        states_filter (list[str]): _description_
        n_points_per_state (int, optional): _description_. Defaults to 250.
        random_seed (int, optional): _description_. Defaults to 42.
        geoshape_filepath (str, optional): _description_. Defaults to "assets/FEATURES/MALHAS/BR_UF_2022.shp".
        output_filepath (str, optional): _description_. Defaults to "assets/INPUT/occurence.parquet".
        state_column_name (str, optional): _description_. Defaults to "SIGLA_UF".
    """
    try:
        br_dataframe: gpd.GeoDataFrame = gpd.read_file(geoshape_filepath)
        br_dataframe = br_dataframe[br_dataframe[state_column_name].isin(states_filter)].cx[:-42,:].reset_index()
        random_points_dataframe = create_dataframe_with_random_points_inside_geom(br_dataframe, n_points=n_points_per_state, seed=random_seed)

        random_points_dataframe['Presence'] = 0
        occurence = pd.read_parquet(occurence_file_path)

        occurence_absence = pd.concat([random_points_dataframe, occurence])
        occurence_absence.to_parquet(output_filepath)

    except Exception as e:
        raise e
    print(f"DOWNLOADED SUCCESS >==> {output_filepath}")
    return

if __name__ == '__main__':
    with open("create_absence_presence_dataframe.toml", "rb") as f:
        config = tomllib.load(f)
    main(**config)
    