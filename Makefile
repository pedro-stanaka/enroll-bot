
deps:
	@brew install python3 poetry
	@poetry install
	@poetry run playwright install --force chromium

run:
	@poetry run main
