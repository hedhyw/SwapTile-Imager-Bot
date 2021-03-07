export UNSPLASH_CLIENT_ID ?=
export UNSPLASH_SLEEP ?= 0
export TELEGRAM_TOKEN ?=
export TELEGRAM_CHATS ?=
export IMAGER_PUBLIC_ADDRESS ?= http://localhost:8081
export IMAGER_INTERNAL_ADDRESS ?= http://localhost:8081
export IMAGER_IMAGE_SIZE ?= 1080x1920
export IMAGER_IMAGE_FORMAT ?= JPEG

run:
	python3 main.py \
		--telegram "$(TELEGRAM_TOKEN)" \
		--unsplash "$(UNSPLASH_CLIENT_ID)" \
		--unsplash-sleep "$(UNSPLASH_SLEEP)" \
		--imager-public "$(IMAGER_PUBLIC_ADDRESS)" \
		--imager-internal "$(IMAGER_INTERNAL_ADDRESS)" \
		--imager-imsize "$(IMAGER_IMAGE_SIZE)" \
		--imager-imformat "$(IMAGER_IMAGE_FORMAT)" \
		--allowed-chats "$(TELEGRAM_CHATS)"
.PHONY: run

prepare:
	pip3 install -r requirements.txt
.PHONY: prepare

lint:
	python3 -m flake8 .
	python3 -m pylint --load-plugins pylint_quotes ./**.py
.PHONY: lint
