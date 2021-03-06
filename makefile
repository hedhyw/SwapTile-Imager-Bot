export UNSPLASH_CLIENT_ID ?=
export TELEGRAM_TOKEN ?=
export IMAGER_ADDR ?= http://localhost:8081

run:
	python3 main.py \
		--telegram "$(TELEGRAM_TOKEN)" \
		--unsplash "$(UNSPLASH_CLIENT_ID)"
		--iamger "$(IMAGER_ADDR)"
.PHONY: run

prepare:
	pip3 install -r requirements.txt
.PHONY: prepare

lint:
	python3 -m flake8 .
	python3 -m pylint --load-plugins pylint_quotes ./**.py
.PHONY: lint
