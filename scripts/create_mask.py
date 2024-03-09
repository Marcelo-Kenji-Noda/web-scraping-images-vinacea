import tomllib
import geopandas as gpd
import os

if __name__ == '__main__':
    HOME = os.path.dirname(os.path.relpath(__file__))
    with open(os.path.join(HOME,"create_mask.toml"), "rb") as f:
        config = tomllib.load(f)
        
    INFOS_UFS = gpd.read_file(config['input_file_path'],  include_fields=['SIGLA_UF','geometry'])
    INFOS_UFS = INFOS_UFS[INFOS_UFS['SIGLA_UF'].isin(config['UFS'])]
    INFOS_UFS = INFOS_UFS.to_crs(4326)
    INFOS_UFS.to_file(config['export_file_path'], driver='GeoJSON')