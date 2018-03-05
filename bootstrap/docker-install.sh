#!/bin/bash
set -euo pipefail

DOCKER_REPO=${DOCKER_REPO:-https://download.docker.com/linux/centos/docker-ce.repo}
DOCKER_CHANNEL=${DOCKER_CHANNEL:-stable}

if rpm -q docker-ce; then
    echo "Docker is already installed"
    exit 0
fi

# Use `yum-config-manager` to configure Docker's yum repository.
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo $DOCKER_REPO
sudo yum-config-manager --enable docker-ce-$DOCKER_CHANNEL
sudo yum makecache
sudo yum install -y docker-ce

# Enable and start the Docker service
sudo systemctl enable docker
sudo systemctl start docker

# Modify invoking user to be apart of the `docker` group.
sudo usermod -a -G docker $USER
