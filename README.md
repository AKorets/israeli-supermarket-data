Israel Supermarket Data: Transform and visualize the data that published by the supermarkets.
=======================================
The data downloading used by [israeli-supermarket-scarpers](https://github.com/erlichsefi/israeli-supermarket-scarpers/) project

[![Pylint](https://github.com/AKorets/israeli-supermarket-data/actions/workflows/pylint.yml/badge.svg)](https://github.com/AKorets/israeli-supermarket-data/actions/workflows/pylint.yml)
[![Pytest](https://github.com/AKorets/israeli-supermarket-data/actions/workflows/pytest.yml/badge.svg)](https://github.com/AKorets/israeli-supermarket-data/actions/workflows/pytest.yml)
Example
-----------
Example of map with that shows statistics of store per city

![Store Per City Map](img/Map.png)

Store per city chart

![Store Per City chart](img/Store_per_city.png)

Quick start
-----------

This set of command, installed the project on your computer, and run it on [jupyter](https://jupyter.org/)

	git clone https://github.com/AKorets/israeli-supermarket-data
	cd israeli-supermarket-data
	python -m venv venv
	venv\Scripts\activate.bat
	pip install -r requirements.txt
	jupyter notebook city_visual.ipynb
