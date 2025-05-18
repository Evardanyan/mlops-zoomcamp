all: integration-test

unit-test:
	pipenv run pytest tests

integration-test: unit-test
	./integration-test.sh