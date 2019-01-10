# TrafficData
Seattle Traffic Data Project

## Purpose
The purpose of this project is to practice data science/engineering using Seattle traffic data.

Some of the longterm goals of the project:
- explore data science/software tools (AzureML, Jupyter Notebooks, Azure Function Apps, etc)
- be able to predict the evening commute hours in advance (eg: this evening's commute will be better or worse than average)
- look for trends over time on the different routes in the region

## Data
- WSDOT API: http://wsdot.com/traffic/api/ 

## Components

### TrafficArchiver
`/src/dotnet/TrafficArchiver`

This is an Azure Function App dedicated to retrieving the current travel times from the WSDOT Travel Times API every 20 minutes.
It stores the data in an Azure Data Explorer (Kusto) table.

### DataViewer
`src/python/jupyter`

A Jupyter Notebook for viewing plots of the data

### Traffic
`src/python/traffic`

Some Python modules for getting data from the DB

### DataArchiver
**DEPRECATING**

`/src/dotnet/DataArchiver`

~~This is an Azure Function App dedicated to retrieving the current travel times from the WSDOT Travel Times API every 20 minutes.~~
~~It stores the data in a SQL table, also in Azure.~~

I'm deprecating this code because it's more complicated than I need right now, deals with SQL rather than Kusto, and is based on Function Apps V1 instead of V2.

## Setup
#### Requirements
##### Python 3.7
- pyodbc
- pandas
- matplotlib
- configparser

Create config file: `TrafficData/_private/db.config`
```
[CONNECTION]
server = <server>
database = <db>
uid = <uid>
dbpassword = <password>
```

## Who
- Trevor Blanarik

