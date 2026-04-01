.PHONY: build-package update-package deploy-test deploy-release clean
export DEFOLD_SDK_VERSION := 1.11.1

# Build package in virtual environment
build-package:
	@echo "Building package in virtual environment..."
	@bash -c '\
	source .venv/bin/activate && \
	pip install -r requirements.txt && \
	python scripts/build.py \
	'

# Update package and generate docs
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

# Deploy to TestPyPI
deploy-test: clean build-package
	@echo "Deploying package to TestPyPI..."
	@bash -c '\
	pip install --upgrade build twine && \
	python -m build && \
	twine check dist/* && \
	twine upload --repository testpypi dist/* \
	'

# Deploy to PyPI (release)
deploy-release: clean build-package
	@echo "Deploying package to PyPI..."
	@bash -c '\
	pip install --upgrade build twine && \
	python -m build && \
	twine check dist/* && \
	twine upload dist/* \
	'

# Clean all build artifacts
clean:
	@echo "Cleaning..."
	rm -rf pydefoldsdk.egg-info
	rm -rf build
	rm -rf dist
	rm -rf .build