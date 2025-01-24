# Chemin vers le fichier docker-compose
COMPOSE_PATH = srcs/docker-compose.yml

# Commandes principales
prune:
	docker system prune -af

up:
	docker-compose -f $(COMPOSE_PATH) up --build -d

down:
	docker-compose -f $(COMPOSE_PATH) down

# Alias pour lancer le projet avec `make`
dev: up
