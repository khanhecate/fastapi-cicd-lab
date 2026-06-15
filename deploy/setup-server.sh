#!/bin/bash
# Run this ONCE on your Amazon Linux EC2 server (as ec2-user) to prepare it.
# Usage: bash setup-server.sh

set -e

echo ">>> Updating system packages..."
sudo dnf update -y

echo ">>> Installing Python3, pip, and git..."
sudo dnf install -y python3 python3-pip git

echo ">>> Cloning repo (you can also do this manually)..."
cd ~
if [ ! -d "fastapi-cicd-lab" ]; then
  echo "Repo not found. Clone it manually first:"
  echo "  git clone <your-repo-url> ~/fastapi-cicd-lab"
  exit 1
fi

cd ~/fastapi-cicd-lab/app

echo ">>> Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
deactivate

echo ">>> Installing systemd service..."
sudo cp ~/fastapi-cicd-lab/deploy/api.service /etc/systemd/system/api.service
sudo systemctl daemon-reload
sudo systemctl enable api
sudo systemctl start api

echo ">>> Done! Check status with: sudo systemctl status api"
echo ">>> Don't forget to open port 8000 in your EC2 Security Group!"