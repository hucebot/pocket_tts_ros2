.PHONY: build run shell

build:
	docker compose build

run:
	docker compose up

shell:
	docker compose run --entrypoint /bin/bash kyutai_tts