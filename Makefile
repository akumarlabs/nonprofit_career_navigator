.PHONY: run lint format test check

# Run the Flask app
run:
	python app.py

# Run flake8 linter
lint:
	flake8 .

# Run black formatter
format:
	black .

# Run unit tests with pytest
test:
	pytest

# Run all checks: format, lint, test
# autoflake --in-place --remove-unused-variables --remove-all-unused-imports -r .
check: format lint test

# Run pre-commit manually on all files
precommit:
	pre-commit run --all-files
