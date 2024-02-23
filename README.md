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
