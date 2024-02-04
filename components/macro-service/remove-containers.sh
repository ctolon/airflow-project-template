#!/bin/bash

# Usage for build with specifying project: build-containers.sh path/to/docker-compose1.yml path/to/docker-compose2.yml
# Usage for build all projects: build-containers.sh

source .env

# Define a cleanup function that stops and removes the Docker containers that were started successfully
function cleanup {
  echo "Cleaning up..."
  for element in "${SUCCESSFUL_REMOVES[@]}"; do
    docker-compose -f "$element" down -v
    echo "Stopped and removed container started from $element"
  done
}

# Define a signal handler that calls the cleanup function when the script receives an interrupt signal
trap cleanup INT

declare -a YAML_PATHS;
declare -a SUCCESSFUL_REMOVES;

echo "Docker Microservice Remover Starting..."

# Check if YAML_PATHS is empty
if [ -z "$@" ]; then
  echo "No path specified. All Docker Microservices will be started."
  YAML_PATHS=()
  for var in $(env | awk -F= '/_YAML_PATH$/ {print $1}'); do
    YAML_PATHS+=("${!var}")
  done
else
  YAML_PATHS=("$@")
fi

# Stop and Remove Containers
for element in "${YAML_PATHS[@]}"
do
  echo "Stopping and removing container for $element.."
  if docker-compose -f "$element" down -v; then
    echo "Stop and remove Successful for $element"
    SUCCESSFUL_REMOVES+=("$element")
  else
    echo "Stop and remove Failed for $element"
    cleanup
    exit 1
  fi
done

echo "All Containers Remove Process Finished Successfully!"