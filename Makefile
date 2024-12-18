SHELL := /bin/bash
install:
	pip install -e .
lint:
	black . --check
	flake8 --config=config/.flake8 src/
	pylint --rcfile=config/.pylintrc src/ || true
unit_tests:
	pytest --cov=hdx_stable_schema --cov-config=config/.coveragerc tests/
