from osgeo import gdal
import tomllib

def update_transform(source_tiff_path, target_tiff_path, output_tiff_path):
    """
    Update the transform of the target GeoTIFF to be exactly the same as the source GeoTIFF
    and save the updated GeoTIFF to a new file.

    Args:
        source_tiff_path (str): Path to the source GeoTIFF file.
        target_tiff_path (str): Path to the target GeoTIFF file to be updated.
        output_tiff_path (str): Path to save the updated GeoTIFF file.

    Returns:
        None
    """
    # Open the source GeoTIFF to get its transform
    source_dataset = gdal.Open(source_tiff_path, gdal.GA_ReadOnly)
    if source_dataset is None:
        raise ValueError(f"Failed to open source GeoTIFF file: {source_tiff_path}")

    # Get the affine transform from the source GeoTIFF
    source_transform = source_dataset.GetGeoTransform()

    # Open the target GeoTIFF to read raster data
    target_dataset = gdal.Open(target_tiff_path, gdal.GA_ReadOnly)
    if target_dataset is None:
        raise ValueError(f"Failed to open target GeoTIFF file: {target_tiff_path}")

    # Get raster band
    band = target_dataset.GetRasterBand(1)

    # Create output GeoTIFF file with the same dimensions and data type as the original
    driver = gdal.GetDriverByName('GTiff')
    output_dataset = driver.Create(output_tiff_path, target_dataset.RasterXSize, target_dataset.RasterYSize,
                                   1, band.DataType)
    if output_dataset is None:
        raise ValueError(f"Failed to create output GeoTIFF file: {output_tiff_path}")

    # Set the affine transform to the output GeoTIFF
    output_dataset.SetGeoTransform(source_transform)

    # Write raster data to the output GeoTIFF
    output_band = output_dataset.GetRasterBand(1)
    output_band.WriteArray(band.ReadAsArray())

    # Set NODATA value
    if band.GetNoDataValue():
        output_band.SetNoDataValue(band.GetNoDataValue())

    # Set the projection (CRS) - copy from source GeoTIFF
    output_dataset.SetProjection(source_dataset.GetProjection())

    # Close the datasets
    source_dataset = None
    target_dataset = None
    output_dataset = None
    
def update_transformv2(source_tiff_path, target_tiff_path, output_tiff_path):
    """
    Update the transform of the target GeoTIFF to be exactly the same as the source GeoTIFF
    and save the updated GeoTIFF to a new file.

    Args:
        source_tiff_path (str): Path to the source GeoTIFF file.
        target_tiff_path (str): Path to the target GeoTIFF file to be updated.
        output_tiff_path (str): Path to save the updated GeoTIFF file.

    Returns:
        None
    """
    # Open the source GeoTIFF to get its transform
    source_dataset = gdal.Open(source_tiff_path, gdal.GA_ReadOnly)
    if source_dataset is None:
        raise ValueError(f"Failed to open source GeoTIFF file: {source_tiff_path}")

    # Open the target GeoTIFF to get its driver
    target_dataset = gdal.Open(target_tiff_path, gdal.GA_ReadOnly)
    if target_dataset is None:
        raise ValueError(f"Failed to open target GeoTIFF file: {target_tiff_path}")
    
    # Get the nodata value from the source dataset
    nodata_value = target_dataset.GetRasterBand(1).GetNoDataValue()
    # Get the driver from the target dataset
    driver = target_dataset.GetDriver()

    # Create a copy of the source GeoTIFF
    output_dataset = driver.CreateCopy(output_tiff_path, source_dataset, strict=0)
    if output_dataset is None:
        raise ValueError(f"Failed to create output GeoTIFF file: {output_tiff_path}")

    # Set the nodata value for the output dataset
    output_band = output_dataset.GetRasterBand(1)
    if nodata_value is not None:
        output_band.SetNoDataValue(nodata_value)
        
    # Close the datasets
    source_dataset = None
    target_dataset = None
    output_dataset = None
    
def main(source_tiff_path: str, target_tiff_path: list[str], output_target_path: list[str]):
    for target_file, output_file_name in zip(target_tiff_path, output_target_path):
        update_transformv2(source_tiff_path, target_file, output_file_name)
        print("Transform updated successfully. Output file saved as:", output_file_name)
    return
if __name__ == '__main__':
    with open("update_transform.toml", "rb") as f:
        config = tomllib.load(f)
    main(**config)
