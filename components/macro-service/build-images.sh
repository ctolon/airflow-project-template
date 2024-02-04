#!/bin/bash

# Usage for build with specifying project: build-images.sh path/to/docker-compose1.yml path/to/docker-compose2.yml
# Usage for build all projects: build-images.sh

source .env

# Define a cleanup function that removes the Docker images that were built successfully
function cleanup {
  echo "Cleaning up..."
  for element in "${SUCCESSFUL_BUILDS[@]}"; do
    docker-compose -f "$element" down -v --rmi local
    echo "Removed image built from $element"
  done
}

# Define a signal handler that calls the cleanup function when the script receives an interrupt signal
trap cleanup INT

declare -a YAML_PATHS;
declare -a SUCCESSFUL_BUILDS;

echo "Docker Microservice Builder Starting..."

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

# Build Images
for element in "${YAML_PATHS[@]}"
do
  echo "Building start for $element.."
  if docker-compose -f "$element" build; then
    echo "Build Successful for $element"
    SUCCESSFUL_BUILDS+=("$element")
  else
    echo "Build Failed for $element"
    cleanup
    exit 1
  fi
done

echo "Building Images Process Finished Successfully!"