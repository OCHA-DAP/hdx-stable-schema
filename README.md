# HDX Stable Schema


## Contributions

For developers the code should be cloned installed from the [GitHub repo](https://github.com/OCHA-DAP/hdx-cli-toolkit), and a virtual enviroment created:

```shell
python -m venv venv
source venv/Scripts/activate
```

And then an editable installation created:

```shell
pip install -e .
```


## Usage

Here are some sample commandlines which explore some datasets containing CSV or XLSX format data:

```
hdx-schema show_schema --dataset_name=climada-litpop-dataset
hdx-schema show_schema --dataset_name=explosive-weapons-use-affecting-aid-access-education-and-healthcare-services
hdx-schema show_schema --dataset_name=who-data-for-mwi
```

This dataset contains both CSV and GeoJSON format data:

```
hdx-schema show_schema --dataset_name=gibraltar-healthsites
```

These datasets just contain GeoJSON and other geographic formats:

```
hdx-schema show_schema --dataset_name=geoboundaries-admin-boundaries-for-nepal
hdx-schema show_schema --dataset_name=hotosm_npl_financial_services
hdx-schema show_schema --dataset_name=kenya_current_situation_fewsnet_ipc_classification
```

Example output from `hdx-schema show_schema --dataset_name=gibraltar-healthsites`

```
******************************************
* Gibraltar Healthsites                  *
* Dataset Overview                       *
* Invoked at: 2024-12-09T11:16:49.420619 *
******************************************
Dataset name: gibraltar-healthsites
Resource list:

 1. gibraltar-healthsites-csv-with-hxl-tags
	Filename: gibraltar_hxl.csv 
	Format: CSV
	Sheets: __DEFAULT__ (n_columns:35 x n_rows:25)
	Checks (1 file structure checks):
		2024-11-25

 2. gibraltar-healthsites-shp
	Filename: gibraltar-shapefiles.zip 
	Format: SHP
	Sheets: __DEFAULT__ (n_columns:35 x n_rows:N/A)
	Bounding box: BOX(-5.360211949624244 36.12558915715644,-5.349349506025561 36.15278843295448)
	Checks (1 file structure checks):
		2024-11-25

 3. gibraltar-healthsites-geojson
	Filename: gibraltar.geojson 
	Format: GeoJSON
	Sheets: __DEFAULT__ (n_columns:35 x n_rows:N/A)
	Bounding box: BOX(-5.360211949624244 36.12558915715644,-5.349349506025561 36.15278843295448)
	Checks (1 file structure checks):
		2024-11-25

 4. gibraltar-healthsites-hxl-geojson
	Filename: gibraltar_hxl.geojson 
	Format: GeoJSON
	Sheets: __DEFAULT__ (n_columns:35 x n_rows:N/A)
	Bounding box: BOX(-5.360211949624244 36.12558915715644,-5.349349506025561 36.15278843295448)
	Checks (1 file structure checks):
		2024-11-25

 5. gibraltar-healthsites-csv
	Filename: gibraltar.csv 
	Format: CSV
	Sheets: __DEFAULT__ (n_columns:35 x n_rows:25)
	Checks (1 file structure checks):
		2024-11-25

Found 5 common schemas

Schema 1, shared by the following 1 resources on sheet '__DEFAULT__':

gibraltar-healthsites-csv-with-hxl-tags  

Data Dictionary
------------------------------------------------------
|Column |Type |Label                      |Description |
------------------------------------------------------
|None   |     |                           |            |
|None   |     |                           |            |
|None   |     |                           |            |
|None   |     |                           |            |
|None   |     |                           |            |
|None   |     |#loc+amenity               |            |
|None   |     |#meta+healthcare           |            |
|None   |     |#loc+name                  |            |
|None   |     |#meta+operator             |            |
|None   |     |#geo+bounds+url            |            |
|None   |     |#meta+speciality           |            |
|None   |     |#meta+operator_type        |            |
|None   |     |#contact+phone             |            |
|None   |     |#status+operational_status |            |
|None   |     |#access+hours              |            |
|None   |     |#capacity+beds             |            |
|None   |     |#capacity+staff            |            |
|None   |     |#meta+health_amenity_type  |            |
|None   |     |#meta+dispensing           |            |
|None   |     |#meta+wheelchair           |            |
|None   |     |#meta+emergency            |            |
|None   |     |#meta+insurance            |            |
|None   |     |#meta+water_source         |            |
|None   |     |#meta+electricity          |            |
|None   |     |#meta+is_in_health_area    |            |
|None   |     |#meta+is_in_health_zone    |            |
|None   |     |#contact+url               |            |
|None   |     |                           |            |
|None   |     |                           |            |
|None   |     |                           |            |
|None   |     |                           |            |
|None   |     |                           |            |
|None   |     |                           |            |
|None   |     |                           |            |
|None   |     |#meta+id                   |            |
------------------------------------------------------

Schema 2, shared by the following 1 resources on sheet '__DEFAULT__':

gibraltar-healthsites-shp  

Data Dictionary
-----------------------------------------------
|Column       |Type         |Label |Description |
-----------------------------------------------
|ogc_fid      |integer      |      |            |
|osm_id       |float        |      |            |
|osm_type     |string       |      |            |
|completene   |string       |      |            |
|amenity      |string       |      |            |
|healthcare   |string       |      |            |
|name         |string       |      |            |
|operator     |string       |      |            |
|source       |string       |      |            |
|speciality   |string       |      |            |
|operator_t   |string       |      |            |
|operationa   |string       |      |            |
|opening_ho   |string       |      |            |
|beds         |string       |      |            |
|staff_doct   |string       |      |            |
|staff_nurs   |string       |      |            |
|health_ame   |string       |      |            |
|dispensing   |string       |      |            |
|wheelchair   |string       |      |            |
|emergency    |string       |      |            |
|insurance    |string       |      |            |
|water_sour   |string       |      |            |
|electricit   |string       |      |            |
|is_in_heal   |string       |      |            |
|is_in_he_1   |string       |      |            |
|url          |string       |      |            |
|addr_house   |string       |      |            |
|addr_stree   |string       |      |            |
|addr_postc   |string       |      |            |
|addr_city    |string       |      |            |
|changeset_   |string       |      |            |
|changese_1   |string       |      |            |
|changese_2   |date         |      |            |
|uuid         |string       |      |            |
|wkb_geometry |user-defined |      |            |
-----------------------------------------------

Schema 3, shared by the following 1 resources on sheet '__DEFAULT__':

gibraltar-healthsites-geojson  

Data Dictionary
------------------------------------------------------
|Column              |Type         |Label |Description |
------------------------------------------------------
|ogc_fid             |integer      |      |            |
|osm_id              |integer      |      |            |
|osm_type            |string       |      |            |
|completeness        |string       |      |            |
|amenity             |string       |      |            |
|healthcare          |string       |      |            |
|name                |string       |      |            |
|operator            |string       |      |            |
|source              |string       |      |            |
|speciality          |string       |      |            |
|operator_type       |string       |      |            |
|operational_status  |string       |      |            |
|opening_hours       |string       |      |            |
|beds                |string       |      |            |
|staff_doctors       |string       |      |            |
|staff_nurses        |string       |      |            |
|health_amenity_type |string       |      |            |
|dispensing          |string       |      |            |
|wheelchair          |string       |      |            |
|emergency           |string       |      |            |
|insurance           |string       |      |            |
|water_source        |string       |      |            |
|electricity         |string       |      |            |
|is_in_health_area   |string       |      |            |
|is_in_health_zone   |string       |      |            |
|url                 |string       |      |            |
|addr_housenumber    |string       |      |            |
|addr_street         |string       |      |            |
|addr_postcode       |string       |      |            |
|addr_city           |string       |      |            |
|changeset_id        |string       |      |            |
|changeset_version   |string       |      |            |
|changeset_timestamp |timestamp    |      |            |
|uuid                |string       |      |            |
|wkb_geometry        |user-defined |      |            |
------------------------------------------------------

Schema 4, shared by the following 1 resources on sheet '__DEFAULT__':

gibraltar-healthsites-hxl-geojson  

Data Dictionary
-------------------------------------------------------------
|Column                     |Type         |Label |Description |
-------------------------------------------------------------
|ogc_fid                    |integer      |      |            |
|osm_id                     |integer      |      |            |
|osm_type                   |string       |      |            |
|completeness               |string       |      |            |
|_loc+amenity               |string       |      |            |
|_meta+healthcare           |string       |      |            |
|_loc +name                 |string       |      |            |
|_meta +operator            |string       |      |            |
|_geo+bounds+url            |string       |      |            |
|_meta +speciality          |string       |      |            |
|_meta +operator_type       |string       |      |            |
|_contact +phone            |string       |      |            |
|_status+operational_status |string       |      |            |
|_access +hours             |string       |      |            |
|_capacity +beds            |string       |      |            |
|_capacity +staff           |string       |      |            |
|_meta +health_amenity_type |string       |      |            |
|_meta+dispensing           |string       |      |            |
|_meta+wheelchair           |string       |      |            |
|_meta+emergency            |string       |      |            |
|_meta+insurance            |string       |      |            |
|_meta+water_source         |string       |      |            |
|_meta+electricity          |string       |      |            |
|_meta+is_in_health_area    |string       |      |            |
|_meta+is_in_health_zone    |string       |      |            |
|_contact +url              |string       |      |            |
|addr_housenumber           |string       |      |            |
|addr_street                |string       |      |            |
|addr_postcode              |string       |      |            |
|addr_city                  |string       |      |            |
|changeset_id               |string       |      |            |
|changeset_version          |string       |      |            |
|changeset_timestamp        |timestamp    |      |            |
|_meta +id                  |string       |      |            |
|wkb_geometry               |user-defined |      |            |
-------------------------------------------------------------

Schema 5, shared by the following 1 resources on sheet '__DEFAULT__':

gibraltar-healthsites-csv  

Data Dictionary
----------------------------------------------
|Column              |Type |Label |Description |
----------------------------------------------
|X                   |     |      |            |
|Y                   |     |      |            |
|osm_id              |     |      |            |
|osm_type            |     |      |            |
|completeness        |     |      |            |
|amenity             |     |      |            |
|healthcare          |     |      |            |
|name                |     |      |            |
|operator            |     |      |            |
|source              |     |      |            |
|speciality          |     |      |            |
|operator_type       |     |      |            |
|operational_status  |     |      |            |
|opening_hours       |     |      |            |
|beds                |     |      |            |
|staff_doctors       |     |      |            |
|staff_nurses        |     |      |            |
|health_amenity_type |     |      |            |
|dispensing          |     |      |            |
|wheelchair          |     |      |            |
|emergency           |     |      |            |
|insurance           |     |      |            |
|water_source        |     |      |            |
|electricity         |     |      |            |
|is_in_health_area   |     |      |            |
|is_in_health_zone   |     |      |            |
|url                 |     |      |            |
|addr_housenumber    |     |      |            |
|addr_street         |     |      |            |
|addr_postcode       |     |      |            |
|addr_city           |     |      |            |
|changeset_id        |     |      |            |
|changeset_version   |     |      |            |
|changeset_timestamp |     |      |            |
|uuid                |     |      |            |
----------------------------------------------
```