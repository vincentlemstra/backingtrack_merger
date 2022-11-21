requirements:
	pip-compile --output-file requirements.txt requirements.in

install:
	pip install -r requirements.txt