#!/bin/bash


set -euox pipefail

# Get an unique venv folder to using *inside* workspace
VENV=".venv-$BUILD_NUMBER"

# Initialize new venv
python3 -m venv "$VENV"

# Update pip
source "$VENV/bin/activate"

pip3 install pipenv
pipenv install --dev --deploy

AWS_ACCOUNT_ID="$(aws sts get-caller-identity  --output=text --query "Account")"

FULL_VERSION_NUMBER="$(python3 setup.py --version)"

VERSION_NUMBER=$(echo $FULL_VERSION_NUMBER| cut -d '+' -f 1)

eval "$(aws ecr get-login --no-include-email --region us-east-1)"

python3 setup.py build

docker build -t concordia .
docker tag concordia:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/concordia:${VERSION_NUMBER}
docker tag concordia:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/concordia:latest
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/concordia:${VERSION_NUMBER}
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/concordia:latest

docker build -t concordia/importer --file importer/Dockerfile .
docker tag concordia/importer:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/concordia/importer:${VERSION_NUMBER}
docker tag concordia/importer:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/concordia/importer:latest
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/concordia/importer:${VERSION_NUMBER}
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/concordia/importer:latest

docker pull rabbitmq:latest
docker tag rabbitmq:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/rabbitmq:${VERSION_NUMBER}
docker tag rabbitmq:latest ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/rabbitmq:latest
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/rabbitmq:${VERSION_NUMBER}
docker push ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com/rabbitmq:latest