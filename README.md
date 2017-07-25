# tsi-mapgen

#### Description

This script is used to generate the "field mapping" JSON required for the incidentTemplate.json configuration file used in the TSI Remedy Plugin as well as the TSI Remedy Bulk Ingestion script.

NOTE: This version only works with SQL Server based Remedy instances but can be adapted for Oracle pretty easily.

#### Pre-Requisites
- Python 3.x
- pymssql (can be tricky to install, use the Googles)
- json
- re

