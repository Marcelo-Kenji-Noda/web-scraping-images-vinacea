import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import tomllib

def generate_occurence_dataset(gbif_raw_file_path:str, gbif_treated_file_path: str, occurence_file_path:str):
    STATE_NAME_ENCODING = {
    "Santa Catarina":"SC",
    "São Paulo":"SP",
    "Rio Grande do Sul":"RS",
    "Minas Gerais":"MG",
    "Paraná":"PR",
    "Espírito Santo":"ES",
    "Brazil - São Paulo":"SP",
    "Rio de Janeiro":"RJ",
    "Brazil - Minas Gerais":"MG",
    "Bahia":"BA",
    "Mato Grosso do Sul":"MS",
    "Parana":"PR",
    "Brazil - Santa Catarina":"SC",
    "Sp":"SP"  
    }
    ## Selecting and transforming data to correct data types
    dtype_dict = {
        'dateIdentified': 'object',
        'day': 'float64',
        'establishmentMeans': 'object',
        'identifiedBy': 'object',
        'mediaType': 'object',
        'month': 'float64',
        'recordNumber': 'object',
        'rightsHolder': 'object',
        'verbatimScientificNameAuthorship': 'object',
        'year': 'float64'
    }

    ## Lendo o arquivo original (gbif.csv) e salvando em um arquivo para ser tratado
    occurence_species_data_unfiltered = pd.read_csv(
        gbif_raw_file_path,
        sep='\t',
        dtype=dtype_dict
    ).reset_index().to_parquet(gbif_treated_file_path)

    ## Selecionando somente as colunas que serão utilizadas no modelo e nas etapas de exploração de dados
    occurence_species_data = pd.read_parquet(
        gbif_treated_file_path, 
        columns=[
            'countryCode',
            'locality',
            'decimalLatitude',
            'decimalLongitude',
            'eventDate',
            'individualCount',
            'basisOfRecord',
            'collectionCode',
            'stateProvince'],
    ).reset_index(drop=True)

    ## Aplicando filtros e regras iniciais
    occurence_species_data = occurence_species_data[occurence_species_data['countryCode'] == 'BR'] # Filtering only in Brazil
    occurence_species_data = occurence_species_data[~occurence_species_data['eventDate'].isna()].reset_index(drop=True) # Removing data that does not contain date information
    occurence_species_data.loc[occurence_species_data['individualCount'].isna(),'individualCount'] = 1 # Caso um dado esteja no arquivo, porém não tenha um contagem de unidades específicas, o dado será considerado como 1 observação
    occurence_species_data = occurence_species_data[occurence_species_data['decimalLatitude'].notna() & occurence_species_data['decimalLongitude'].notna()] # Removing data without any information about latitude and longitude
    occurence_species_data['eventDate'] = pd.to_datetime(occurence_species_data['eventDate'], format="mixed", utc=True) # Setting column as datetime
    occurence_species_data.loc[:,'stateProvince'] = occurence_species_data.stateProvince.replace(STATE_NAME_ENCODING) # Padronizando o nome dos estados
    occurence_species_data = occurence_species_data[~occurence_species_data['stateProvince'].isnull()].reset_index(drop=True) # Removendo linhas que não contém a informação de estado

    COLUMNS_RENAME = {
        "countryCode":"Pais",
        "locality":"Localizacao",
        "decimalLatitude":"Latitude",
        "decimalLongitude":"Longitude",
        "eventDate":"Data",
        "individualCount":"Contagem de individuos",
        "collectionCode":"Plataforma",
        "stateProvince":"Estado",
        "basisOfRecord":"Fonte do registro"
    }

    # Renomeando os arquivos e criando a variável alvo "Presence"
    occurence_species_data.rename(columns=COLUMNS_RENAME, inplace=True)
    occurence_species_data.to_parquet(gbif_treated_file_path, index=False)
    occurence_species_data['Presence'] = 1
    occurence = occurence_species_data[['Latitude','Longitude','Presence']].copy()

    ## São criados dois arquivos nesse momento, o occurence_file e o gbif_treated
    ## O primeiro arquivo contém somente as informações de latitude, longitude e presença, que será utilizado no modelo
    ## O segundo arquivo contém todas as informações tratadas para que seja possível realizar uma análise exploratória dos dados
    occurence.to_parquet(occurence_file_path, index=False)
    
    print(f"CREATED {occurence_file_path}")
    return

if __name__ == '__main__':
    with open("create_occurence_dataset.toml", "rb") as f:
        config = tomllib.load(f)
    generate_occurence_dataset(**config)
