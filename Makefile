.PHONY: build-package update-package deploy-test deploy-release clean

export DEFOLD_SDK_VERSION := 1.12.1

all: clean build-version build-package update-package deploy-test deploy-release clean

build-version:
	echo $(DEFOLD_SDK_VERSION) > VERSION

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
		if [ -d "docs" ]; then rm -rf docs/*.md; fi && \
		source .venv/bin/activate && \
		python scripts/gendoc.py \
	'

deploy-test: clean build-package
	@echo "Deploying package to TestPyPI..."
	@bash -c '\
		source .venv/bin/activate && \
		pip install --upgrade build twine && \
		python -m build && \
		twine check dist/* && \
		twine upload --repository testpypi dist/*  --verbose  \
	'

deploy-release: clean build-package
	@echo "Deploying package to PyPI..."
	@bash -c '\
		source .venv/bin/activate && \
		pip install --upgrade build twine && \
		python -m build && \
		twine check dist/* && \
		twine upload dist/* \
	'

clean:
	@echo "Cleaning..."
	rm -rf pydefoldsdk.egg-info
	rm -rf build
	rm -rf dist
	rm -rf .build

