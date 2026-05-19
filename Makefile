.PHONY: dev test lint build deploy

dev:           ## Start local dev stack
	docker compose up --build

test:          ## Run tests locally
	cd api && pytest tests/ -v --cov=app

lint:          ## Lint + format check
	ruff check api/ && ruff format --check api/

migrate:       ## Run DB migrations
	docker compose exec api alembic upgrade head

logs:          ## Tail API logs
	docker compose logs -f api

clean:         ## Remove containers + volumes
	docker compose down -v --remove-orphans