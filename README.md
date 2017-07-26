# tsi-mapgen

#### Description

This script is used to generate the "field mapping" and "properties" JSON required for the incidentTemplate.json configuration file used in the TSI Remedy Plugin as well as the TSI Remedy Bulk Ingestion script.

There are two files created:

1) properties.json - this contains the "properties" section of the file
2) map.json - this contains the field mappings directly following the properties

TODO: Modify the code to output a single json file!
NOTE: This version only works with SQL Server based Remedy instances but can be adapted for Oracle pretty easily.

#### Pre-Requisites
- Python 3.x
- pymssql (can be tricky to install, use the Googles)
- json
- re

