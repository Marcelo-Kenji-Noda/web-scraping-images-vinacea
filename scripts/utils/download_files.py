import requests
import zipfile
import io

def download_zip_file_content(input_file_path: str, output_file_path: str) -> None:
    """
    Download zip file
    Args:
        input_file_path (str): File path 
        output_file_path (str): Output path
        
    Example:
        input_file_path: str = "http://www.dsr.inpe.br/topodata/data/geotiff/23S435SN.zip"
        output_file_path: str = "/mnt/biofeats/assets/TOPOGRAPHY/"
        download_zip_file(input_file_path = input_file_path, output_file_path = output_file_path)
    """
    r = requests.get(input_file_path)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(output_file_path)
    return


def download_zip_file(input_file_path: str, output_file_path: str) -> None:
    """
    Download zip file
    Args:
        input_file_path (str): File path 
        output_file_path (str): Output path
        
    Example:
        input_file_path: str = "http://www.dsr.inpe.br/topodata/data/geotiff/23S435SN.zip"
        output_file_path: str = "/mnt/biofeats/assets/TOPOGRAPHY/"
        download_zip_file(input_file_path = input_file_path, output_file_path = output_file_path)
    """
    r = requests.get(input_file_path)
    with open(output_file_path, 'wb') as f:
        # Write the content of the response to the local file
        f.write(r.content)
    return