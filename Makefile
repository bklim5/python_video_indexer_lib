install:
	pip install -r requirements.txt

install-dev: install
	pip install -r requirements-test.txt

lint:
	flake8 video_indexer tests

component:
	PYTHONPATH=./video_indexer:. pytest -sv tests/

coverage:
	PYTHONPATH=./video_indexer:. pytest tests/ --cov=video_indexer

test: lint component

cleanup-build:
	rm -rf ./build
	rm -rf ./dist
	python setup.py sdist bdist_wheel

pypi-dev: cleanup-build
	python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

pypi: cleanup-build
	python -m twine upload dist/*
