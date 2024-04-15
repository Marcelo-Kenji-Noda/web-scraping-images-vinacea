import matplotlib.pyplot as plt
import rasterio

def plot_tif(tif_file):
    # Open the GeoTIFF file
    with rasterio.open(tif_file) as src:
        # Read the raster data
        raster_data = src.read(1)  # Assuming it's a single-band raster
        
        # Get the spatial extent of the raster
        extent = [src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top]
        print(src.bounds)
        # Plot the raster data
        plt.figure(figsize=(10, 10))
        plt.imshow(raster_data, extent=extent, cmap='terrain')
        plt.colorbar(label='Elevation')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Elevation Map')
        plt.show()

# Example usage
tif_file = "../generated_files/mantiqueira_cropped/altitude_br.tif"
plot_tif(tif_file)