import dask.dataframe as dd
import pandas as pd

if __name__ == '__main__':
    FILE_PATH = "../assets/gbif.csv"
    OUTPUT_FILE_PATH = "../assets/gibf.parquet"
    
    #Dicionário utilizado para padronizar o nome dos estados
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
    
## Transformando o arquivo em um objeto .parquet
occurence_species_data_unfiltered = dd.read_csv(
       FILE_PATH,
       sep='\t',
       dtype={'dateIdentified': 'object',
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
).reset_index().compute().to_parquet(OUTPUT_FILE_PATH)

occurence_species_data = pd.read_parquet(
    OUTPUT_FILE_PATH, 
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

occurence_species_data = occurence_species_data[occurence_species_data['countryCode'] == 'BR'] # Filtering only in Brazil
occurence_species_data = occurence_species_data[~occurence_species_data['eventDate'].isna()].reset_index(drop=True) # Removing data that does not contain date information
occurence_species_data.loc[occurence_species_data['individualCount'].isna(),'individualCount'] = 1 # Setting 1 as default
occurence_species_data = occurence_species_data[occurence_species_data['decimalLatitude'].notna() & occurence_species_data['decimalLongitude'].notna()] # Removing data without any information about latitude and longitude
occurence_species_data['eventDate'] = pd.to_datetime(occurence_species_data['eventDate'], format="mixed", utc=True) # Setting column as datetime
occurence_species_data.loc[:,'stateProvince'] = occurence_species_data.stateProvince.replace(STATE_NAME_ENCODING) # Renaming