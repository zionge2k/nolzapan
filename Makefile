DC=docker-compose -f docker-compose.yaml -f mongo-docker-compose.yaml

prepare:
	$(DC) up -d mongodb

build:
	$(DC) build $(service) --no-cache

down:
	$(DC) down --remove-orphans

up: prepare
	[[ -z "$(service)" ]] && { $(DC) up $$($(DC) config --services | grep -Ev '(mongo)'); true; } || $(DC) up $(service)

ps:
	$(DC) ps

rib:
	@[[ -z "$(service)" ]] && { echo "service=foo required"; exit 1; } || true
	$(DC) run --service-ports -it $(service) bash

sh:
	@[[ -z "$(service)" ]] && { echo "service=foo required"; exit 1; } || true
	$(DC) exec -it $(service) bash

logs:
	$(DC) logs $(service)

format:
	poetry run black ./api && poetry run isort ./api
