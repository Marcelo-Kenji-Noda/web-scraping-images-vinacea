from download_files import download_zip_file

input_file_path: str = "http://www.dsr.inpe.br/topodata/data/geotiff/23S435SN.zip"
output_file_path: str = "../assets/TILE/23S435SN.zip"

download_zip_file(input_file_path = input_file_path, output_file_path = output_file_path)