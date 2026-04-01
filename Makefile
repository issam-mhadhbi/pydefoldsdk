.PHONY: build-package update-package
export DEFOLD_SDK_VERSION := 1.11.1


build-package:
	@echo "Building package in virtual environment..."
	@bash -c '\
	source .venv/bin/activate && \
	pip install -r requirements.txt && \
	python scripts/build.py \
	'

update-package:
	@echo "Updating package..."
	@bash -c '\
	if [ -d "pydefoldsdk" ]; then rm -rf pydefoldsdk; fi && \
	cp -r .build/pydefold-*/pydefoldsdk . && \
	if [ -d "docs" ]; then rm -rf docs; fi && \
	mkdir docs && \
	source .venv/bin/activate && \
	python scripts/gendoc.py \
	'

deploy-package : 
	pip install twine requests setuptools
	rm -rf dist *.egg-info || true
	python setup.py sdist  bdist_wheel 