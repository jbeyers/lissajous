
help:
	echo "see the file for help"

pip:
	pip install --upgrade pip pip-tools

up: pip
	pip-compile --upgrade requirements.in
	
deps: pip
	pip-sync


run:
	echo "open http://localhost:8000/"
	flask run --port=8000 --debug