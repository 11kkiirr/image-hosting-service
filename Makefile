run dev:
	cd backend/src && uv run uvicorn main:app --reload

check:
	cd backend/src && uv run ruff check

checkf:
	cd backend/src && uv run ruff check --fix

format:
	cd backend/src && uv run ruff format

lint:
	cd backend/src && uv run pyright .

test:
	pytest tests/ 
