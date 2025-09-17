start:
	pip freeze > requirements.txt && chmod +x predstart.sh && ./predstart.sh && sudo docker compose up --build
clean:
	sudo docker system prune -af --volumes
test:
	pytest -v --cache-clear --color=yes --cov -n auto