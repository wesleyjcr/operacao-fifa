SHELL := /bin/bash

install:
	pip install --upgrade pip
	pip install -r requirements.txt
	pip install -r requirements_dev.txt

uninstall:
	pip uninstall -y -r requirements.txt
	pip uninstall -y -r requirements_dev.txt

build:
	echo "build"

test:
	echo "test"

inspect:
	echo "inspect"

run:
	flask run

publish:
	echo "publish"

commit:
	echo "commit"

release:
	echo "cria uma versão/changelog dos n commits desde o último release"