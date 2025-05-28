# Makefile for spending-money-on-apis

# Default shell
SHELL := /bin/bash

# Python interpreter
PYTHON := python
UV := uv

# Directories
SRC_DIR := src/spending_money_on_apis
TEST_DIR := tests
EXAMPLES_DIR := examples
OUTPUT_DIR := output

# Default target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  make setup        - Set up the project environment"
	@echo "  make install      - Install dependencies"
	@echo "  make test         - Run all tests"
	@echo "  make check-config - Check configuration and API keys"
	@echo "  make format       - Format code with black"
	@echo "  make lint         - Lint code with ruff"
	@echo "  make clean        - Clean generated files"
	@echo "  make google-maps  - Run Google Maps example"
	@echo "  make cborg        - Run CBORG API example"
	@echo "  make all-examples - Run all API examples"

# Setup project
.PHONY: setup
setup:
	@echo "Setting up project..."
	$(UV) venv --python 3.11
	@echo "✓ Virtual environment created"
	@echo "Run 'source .venv/bin/activate' to activate"

# Install dependencies
.PHONY: install
install:
	@echo "Installing dependencies..."
	$(UV) pip install -e ".[dev]"
	@echo "✓ Dependencies installed"

# Run tests
.PHONY: test
test:
	@echo "Running tests..."
	$(UV) run pytest -v

# Check configuration
.PHONY: check-config
check-config:
	@echo "Checking configuration..."
	$(UV) run $(PYTHON) tests/test_config.py

# Format code
.PHONY: format
format:
	@echo "Formatting code..."
	$(UV) run black .
	@echo "✓ Code formatted"

# Lint code
.PHONY: lint
lint:
	@echo "Linting code..."
	$(UV) run ruff check .

# Clean generated files
.PHONY: clean
clean:
	@echo "Cleaning generated files..."
	rm -rf $(OUTPUT_DIR)
	rm -f *.png *.jpg
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	@echo "✓ Cleaned"

# Create output directory
$(OUTPUT_DIR):
	mkdir -p $(OUTPUT_DIR)

# Run Google Maps example
.PHONY: google-maps
google-maps: $(OUTPUT_DIR)
	@echo "Running Google Maps example..."
	$(UV) run $(PYTHON) $(EXAMPLES_DIR)/google_maps_example.py

# Run CBORG API example
.PHONY: cborg
cborg:
	@echo "Running CBORG API example..."
	$(UV) run $(PYTHON) $(EXAMPLES_DIR)/cborg_api.py

# Run all examples
.PHONY: all-examples
all-examples: google-maps cborg
	@echo "✓ All examples completed"

# Development workflow - format, lint, and test
.PHONY: dev
dev: format lint test
	@echo "✓ Development checks passed"

# Check if local/.env exists
.PHONY: check-env
check-env:
	@if [ ! -f local/.env ]; then \
		echo "Warning: local/.env not found!"; \
		echo "Copy local/.env.template to local/.env and add your API keys"; \
		exit 1; \
	fi

# Quick test - check config and run tests
.PHONY: quick
quick: check-env check-config test

# Full check - everything before committing
.PHONY: pre-commit
pre-commit: check-env format lint test
	@echo "✓ Ready to commit"

# Show current API costs estimate
.PHONY: costs
costs:
	@echo "API Costs (approximate):"
	@echo "- Google Static Maps: \$$0.002 per request (after \$$200/month free)"
	@echo "- CBORG API: Check your plan at cborg.lbl.gov"
	@if [ -d $(OUTPUT_DIR) ]; then \
		echo ""; \
		echo "Generated files:"; \
		ls -lh $(OUTPUT_DIR)/*.png 2>/dev/null | wc -l | xargs echo "  Static maps:"; \
	fi

.DEFAULT_GOAL := help
