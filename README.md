# Pipeline para modelo de distribuição de espécies

## Fonte dos dados:
Ocorrências:
- https://www.gbif.org

Temperatura:
- https://www.worldclim.org/data/worldclim21.html

Vegetacao:
- https://www.earthenv.org/landcover

AmbData:
- https://www.dpi.inpe.br/Ambdata/sistema_coordenadas.php

## Tratamento dos dados

Antes de incluir essas informações no trabalho, é importante reforçar o guia de citação exigido pelo gbif.

Tratamento do arquivo gerado a partir do gbif.com

1- Foram filtrados somente as ocorrências no Brasil
2- Removido as linhas que não continham informações a respeito da data de observação
3- Observações sem "Contagem individual" foram definidas como 1 por padrão
4- Removido as linhas que não continham informação de latitude e longitude
5- Padronizado o nome dos estados na coluna de state province
6- Renomeado as colunas para um padrão mais facilmente legível

COLUNAS:

    "countryCode":"Pais",
    "locality":"Localizacao",
    "decimalLatitude":"Latitude",
    "decimalLongitude":"Longitude",
    "eventDate":"Data",
    "individualCount":"Contagem de individuos",
    "collectionCode":"Plataforma",
    "stateProvince":"Estado",
    "basisOfRecord":"Fonte do registro"

Número total de linhas: 2847

## Pipeline

Pre requisitos para executar os scripts:

Baixar e extrair os arquivos correspondente as variáveis ambientais e adicionar ao caminho no arquivo config.toml dentro da pasta de scripts. Todos os arquivos baixados foram na resolução de 1km

### 1 - create_occurence_dataset.py
Essa etapa do pipeline realiza o tratamento dos dados

#### Configs:
- **gbif_raw_file_path**: Caminho do arquivo a ser tratado
- **gbif_treated_file_path**: Arquivo exportado em formato diferente
- **occurence_file_path**: Arquivo de saída contendo apenas as coordenadas de cada ocorrência
  
### 2 - create_abscence_presence_dataframe.py
- **occurence_file_path**: Arquivo contendo as coordenadas de ocorrência gerado na etapa anterior
- **states_filter**: Lista com os estados no qual os dados serão 
- **n_points_per_state**: Número de pontos a ser gerado
- **random_seed**: Semente para gerar os números aleatórios
- **geoshape_filepath**= Caminho para o arquivo .shp com os estados brasileiros
- **output_filepath**: Caminho com o nome do arquivo que será gerado
- **state_column_name**: Coluna que identifica os estados no arquivo .shp

### 3 - export_geojson_file_from_dataframe.py
- **occurence_absence_file_path**: Caminho com o nome do arquivo que foi gerado na última etapa do pipeline
- **geojson_output_file_path**: Arquivo com os pontos de ocorrência-absencia no formato geojson

### 4 - mask_tiff_file_from_coordinates_list.py
- **geojson** Arquivo com os pontos de ocorrência-absencia geojson gerado na última etapa do pipeline
- **occurence_absence_dataframe_path**: Caminho com o arquivo de presença absencia
- **output_file_path**: Caminho para o arquivo que será gerado com os pontos de ocorrência junto das features
- **explanatory_rasters**: Lista com as variáveis de predição
- **columns**: Nome dado a cada coluna da variável de predição (A sequência deve ser a mesma da definida na variavel explanatory_raster)

### 5 - update_transform.py
- **source_tiff_path**: Arquivo de referência
- **target_tiff_path**: Lista com a entrada dos arquivos que - devem ser transformados
**output_target_path**: Lista com a saida dos arquivos transformados
### 6 - crop_targets_tiff_file.py
- **tiff_files**: Arquivos com as features
- **tiff_output_files**: Arquivo com as features recortadas pelo shape
- **shape_file**: Arquivo com o shape que será utilizado como máscara
### 7 - features_selection.ipynb
- Análise das features que serão selecionadas para ajustar o modelo
### 8 - building_models.ipynb
- Realizando o ajuste do modelo