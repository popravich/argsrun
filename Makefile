
test: flake
	python3 -m unittest discover -v tests

cov: flake
	coverage run --source=argsrun -m unittest discover -v tests
	coverage html
	coverage report

flake:
	pyflakes argsrun tests
	pep8 argsrun tests

.PHONY: test flake cov
