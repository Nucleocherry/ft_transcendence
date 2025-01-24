# Nom du fichier Docker Compose
DOCKER_COMPOSE_FILE = docker-compose.yml

# Commandes principales
prune:
	docker system prune -af

build_up:
	docker-compose -f $(DOCKER_COMPOSE_FILE) up --build -d

down:
	docker-compose -f $(DOCKER_COMPOSE_FILE) down

# Alias pour les commandes
prune_alias: prune
make: build_up
down_alias: down
