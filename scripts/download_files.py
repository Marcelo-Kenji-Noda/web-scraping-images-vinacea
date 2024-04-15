import os
import requests
import numpy as np

# Função para gerar os códigos de quadrícula para uma área delimitadora
def generate_grid_codes(lat_range, lon_range):
    grid_codes = []
    for lat in range(lat_range[0], lat_range[1]):
        for lon in np.arange(lon_range[0], lon_range[1], 1.5):
            lat_str = f'{abs(lat)}' + ('S' if lat < 0 else 'N')
            lon_str = f'{abs(int(np.floor(lon))):02d}' + ('_' if lon % 1 == 0 else '5')

            grid_code = f'{lat_str}{lon_str}'
            grid_codes.append(grid_code)
    return grid_codes

if __name__ == '__main__':
    # Define a área delimitadora
    lat_range = (-33,-17)
    lon_range = (-59, -40)


    # Gerar os códigos de quadrícula para a área delimitadora
    grid_codes = generate_grid_codes(lat_range, lon_range)

    # URL base para download dos tiles
    base_url = 'http://www.dsr.inpe.br/topodata/data/geotiff'

    # Diretório para salvar os tiles baixados
    download_dir = '../assets/TILE'
    os.makedirs(download_dir, exist_ok=True)

    # Baixar os tiles correspondentes aos códigos de quadrícula gerados
    for grid_code in grid_codes[:100]:
        tile_url = f"{base_url}/{grid_code}ZN.zip"
        print('Baixando:', tile_url)
        
        # Enviar uma solicitação GET para a URL do tile
        response = requests.get(tile_url)
        
        # Verificar se a solicitação foi bem-sucedida (código de status 200)
        if response.status_code == 200:
            # Salvar o conteúdo da resposta em um arquivo no diretório de download
            with open(os.path.join(download_dir, f"{grid_code}.tif"), 'wb') as f:
                f.write(response.content)
            print('Download bem-sucedido:', grid_code)
        else:
            print('Falha ao baixar:', grid_code)