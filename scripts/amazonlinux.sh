#!/bin/bash

# This script was created for CentOS.
# You have to run this script using sudo.
# Please refer to https://github.com/Jennas-Lee/training-deployment-jsp-system for details.

# Variables
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
LIGHT_BLUE='\033[0;31m'
NC='\033[0m'
ERROR_MESSAGE="${RED}Failed! If the error is repeated, please leave the issue in https://github.com/Jennas-Lee/training-deployment-jsp-system/issues with this log.${NC}"

# Check user
if (($EUID != 0)); then
  echo "${RED}This script must be run as root.${NC}"
  exit 9
fi

# Read MySQL Root Password
echo -e "${YELLOW}Please Enter MySQL Password : ${NC}"
read mysql_password

echo -e "${YELLOW}Please Confirm MySQL Password : ${NC}"
read confirm_mysql_password

if (($mysql_password != $confirm_mysql_password)); then
  echo "${RED}Password not match. Stop to configuration.${NC}"
  exit 9
fi
export mysql_password

# Start configure
echo -e "${LIGHT_BLUE}Start configure${NC}"

# Start installing docker
echo -e "${LIGHT_BLUE}Start installing docker${NC}"

# Update yum packages
echo -e "${YELLOW}Update yum packages${NC}"
yum update -y
if [ $? -eq 0 ]; then
  echo -e ERROR_MESSAGE
  exit 9
fi

# Install docker
echo -e "${YELLOW}Install docker${NC}"
amazon-linux-extras install docker
if [ $? -eq 0 ]; then
  echo -e ERROR_MESSAGE
  exit 9
fi

# Install docker compose
echo -e "${YELLOW}Install docker compose${NC}"
curl -L "https://github.com/docker/compose/releases/download/1.28.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
if [ $? -eq 0 ]; then
  echo -e ERROR_MESSAGE
  exit 9
fi

# Give a permission
chmod +x /usr/local/bin/docker-compose
if [ $? -eq 0 ]; then
  echo -e ERROR_MESSAGE
  exit 9
fi

# Start docker daemon
echo -e "${YELLOW}Start docker daemon${NC}"
systemctl start docker
if [ $? -eq 0 ]; then
  echo -e ERROR_MESSAGE
  exit 9
fi

systemctl enable docker
if [ $? -eq 0 ]; then
  echo -e ERROR_MESSAGE
  exit 9
fi

# Pull container images
echo -e "${YELLOW}Pull container images${NC}"
docker pull public.ecr.aws/nginx/nginx:1.21.1-alpine
if [ $? -eq 0 ]; then
  echo -e ERROR_MESSAGE
  exit 9
fi

docker tag public.ecr.aws/nginx/nginx:1.21.1-alpine nginx:latest
if [ $? -eq 0 ]; then
  echo -e ERROR_MESSAGE
  exit 9
fi

docker pull public.ecr.aws/bitnami/tomcat:9.0.52
if [ $? -eq 0 ]; then
  echo -e ERROR_MESSAGE
  exit 9
fi

docker tag public.ecr.aws/bitnami/tomcat:9.0.52 tomcat:latest
if [ $? -eq 0 ]; then
  echo -e ERROR_MESSAGE
  exit 9
fi

docker pull public.ecr.aws/bitnami/mysql:8.0.26
if [ $? -eq 0 ]; then
  echo -e ERROR_MESSAGE
  exit 9
fi

docker tag public.ecr.aws/bitnami/mysql:8.0.26 mysql:latest
if [ $? -eq 0 ]; then
  echo -e ERROR_MESSAGE
  exit 9
fi

docker pull ghcr.io/Jennas-Lee/training-deployment-jsp-system:latest
if [ $? -eq 0 ]; then
  echo -e ERROR_MESSAGE
  exit 9
fi

docker tag ghcr.io/Jennas-Lee/training-deployment-jsp-system:latest web:latest
if [ $? -eq 0 ]; then
  echo -e ERROR_MESSAGE
  exit 9
fi

echo -e "${LIGHT_BLUE}Start running primary containers${NC}"
echo -e "${YELLOW}Download docker compose file${NC}"
curl -O https://raw.githubusercontent.com/Jennas-Lee/training-deployment-jsp-system/master/docker-compose.yml
if [ $? -eq 0 ]; then
  echo -e ERROR_MESSAGE
  exit 9
fi

echo -e "${YELLOW}Download NGINX configuration file${NC}"
mkdir /nginx
curl https://raw.githubusercontent.com/Jennas-Lee/traiing-deployment-jsp-system/master/nginx/nginx.conf
if [ $? -eq 0 ]; then
  echo -e ERROR_MESSAGE
  exit 9
fi
mkdir /mysql

docker-compose up -d
if [ $? -eq 0 ]; then
  echo -e ERROR_MESSAGE
  exit 9
fi

echo -e "${GREEN}Successfully install!${NC}"
