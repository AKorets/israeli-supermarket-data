Israel Supermarket Data: Transform and visualize the data that published by the supermarkets.
=======================================
The data downloading used by [erlichsefi/israeli-supermarket-scarpers](https://github.com/erlichsefi/israeli-supermarket-scarpers/) project

All data is based on the government's project for price transparency.
    שקיפות מחירים (השוואת מחירים) - https://www.gov.il/he/departments/legalInfo/cpfta_prices_regulations  
The current state of the original data is a mess that contains a bunch of XML with different schemas and encodings.   
The main goal of this project is to make the data accessible and in one format ([pandas](https://pandas.pydata.org/docs/index.html) csv)

[![Pylint](https://github.com/AKorets/israeli-supermarket-data/actions/workflows/pylint.yml/badge.svg)](https://github.com/AKorets/israeli-supermarket-data/actions/workflows/pylint.yml)
[![Pytest](https://github.com/AKorets/israeli-supermarket-data/actions/workflows/pytest.yml/badge.svg)](https://github.com/AKorets/israeli-supermarket-data/actions/workflows/pytest.yml)  
Example
-----------
An example of a map that shows statistics on stores per city (city_visual.ipynb)

![Store Per City Map](img/Map.png)

Store per city chart (city_visual.ipynb)

![Store Per City chart](img/Store_per_city.png)

Example of item data

	from price_parser import download_all_prices
	
	df = download_all_prices()
	df1.tail(6)

|          |provider     |       chainid |  subchainid |   storeid | itemcode | itemname |   itemprice |   unitqty |   unitofmeasureprice |   qtyinpackage | manufacturename   | manufacturecountry   | manufactureitemdescription           |   bisweighted |   allowdiscount | priceupdatedate     |   unitmeasure |   quantity |
| --------- | --------- | ------------- | ------------- |------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| 7075218 | ZolVeBegadol | 7290058173198 |            1 |        89 | 8719200998049 | מזולה בטעם טבעי                      |        10.9 |     00000 |                0.109 |              0 | לא ידוע           | ישראל                | מזולה בטעם טבעי                      |             0 |               0 | 2021-10-27 10:43:45 |         00000 |          0 |
| 7075219 | ZolVeBegadol | 7290058173198 |            1 |        89 | 8720608014958 | תה ליפטון 1.5 גר' 100 יחידות         |        15.9 |     00000 |                0.159 |             12 | לא ידוע           | הודו                 | תה ליפטון 1.5 גר' 100 יחידות         |             0 |               0 | 2023-07-13 11:22:53 |         00000 |         12 |
| 7075220 | ZolVeBegadol | 7290058173198 |            1 |        89 | 8801055707966 | קפה בריסטה קלוי וטחון                |        36.9 |     00000 |                0.369 |             12 | לא ידוע           | לא ידוע              | קפה בריסטה קלוי וטחון                |             0 |               0 | 2023-05-28 09:59:11 |         00000 |         12 |
| 7075221 | ZolVeBegadol | 7290058173198 |            1 |        89 | 8801055709465 | נסקפה קפוצ'ינו וניל 10 יח' 185 גרם   |        21.5 |     00000 |                0.215 |              0 | לא ידוע           | דרום קוריאה          | נסקפה קפוצ'ינו וניל 10 יח' 185 גרם   |             0 |               0 | 2023-05-28 09:52:11 |         00000 |          0 |
| 7075222 | ZolVeBegadol | 7290058173198 |            1 |        89 | 8801055709489 | נסקפה קפוצ'ינו אגוזים 10 יח' 180 גרם |        21.5 |     00000 |                0.215 |              0 | לא ידוע           | דרום קוריאה          | נסקפה קפוצ'ינו אגוזים 10 יח' 180 גרם |             0 |               0 | 2023-05-28 09:52:12 |         00000 |          0 |
| 7075223 | ZolVeBegadol | 7290058173198 |            1 |        89 | 8850389105832 | סאפה תפוח ליטר                       |        12.7 |     00000 |               12.7   |              0 | לא ידוע           | תאילנד               | סאפה תפוח ליטר                       |             0 |               0 | 2023-05-25 16:54:56 |         00000 |          0 |


Example of store data

	from store_df_parser import download_all_stores
	df = download_all_stores()
 	df.head(4)
 
|     | provider   |   bikoretno |       chainid | zipcode   |   storeid | lastupdatedate      |   storetype | storename            |   subchainid | city   | address           |
|----:|:-----------|------------:|--------------:|:----------|----------:|:--------------------|------------:|:---------------------|-------------:|:-------|:------------------|
|   0 | bareket    |         nan | 7290875100001 | 5621807   |         2 | 31/07/2022 16:23:32 |           1 | 2 יהוד               |            1 | יהוד   | התעשייה 29        |
|  14 | ybitan     |           5 | 7290725900003 | 7860132   |         2 | 2023-07-29          |           1 | אשקלון החאן          |            1 | אשקלון | הרצל 33           |
|  63 | Dor Alon   |           3 | 7290492000005 | unknown   |       595 | 2023-07-27          |           1 | AM-PMזבוטינסקי בת ים |            0 | בת ים  | זבוטינסקי 2 בת ים |
| 621 | GoodPharm  |           9 | 7290058197699 | 4243006   |        44 | 2023-07-29          |           1 | נתניה - חדש הרצל 23  |            1 | נתניה  | הרצל 23           |

Quick start
-----------

This set of command, installed the project on your computer, and run it on [jupyter](https://jupyter.org/)

	git clone https://github.com/AKorets/israeli-supermarket-data
	cd israeli-supermarket-data
	python -m venv venv
	venv\Scripts\activate.bat
	pip install -r requirements.txt
	jupyter notebook city_visual.ipynb

