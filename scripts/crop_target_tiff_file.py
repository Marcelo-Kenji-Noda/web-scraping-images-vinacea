import rasterio
from rasterio.mask import mask
import numpy as np
import geopandas as gpd
import os
import tomllib

def mask_tiff_with_shapefile(tiff_file: str, geoframe: gpd.GeoDataFrame, output_file_name: str,):
    # Abre o arquivo .tiff
    with rasterio.open(tiff_file) as src:
        # Máscara do arquivo .tiff usando o shapefile
        out_image, out_transform = mask(src, geoframe.geometry, crop=True)
        
        # Atualiza os metadados para refletir a nova forma e posição do recorte
        out_meta = src.meta.copy()
        out_meta.update({"driver": "GTiff",
                        "height": out_image.shape[1],
                        "width": out_image.shape[2],
                        "transform": out_transform})
        
        # Aplicar uma máscara adicional para remover os valores nodata
        # out_image = np.ma.masked_where(out_image == src.nodata, out_image)
    
        # Salva o recorte em um novo arquivo .tiff
        with rasterio.open(output_file_name, "w", **out_meta) as dest:
            dest.write(out_image)
    return output_file_name

def main(tiff_files: list[str], tiff_output_files: list[str], shape_file: str):
    geoframe = gpd.read_file(shape_file)
    for tiff_file, tiff_output_file in zip(tiff_files, tiff_output_files):
        mask_tiff_with_shapefile(tiff_file=tiff_file,geoframe=geoframe, output_file_name=tiff_output_file)
    return

if __name__ == '__main__':
    with open("crop_target_tiff_file.toml", "rb") as f:
        config = tomllib.load(f)
    main(**config)