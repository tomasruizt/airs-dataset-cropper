#!/usr/bin/env bash
sudo add-apt-repository ppa:jonathonf/python-3.6 -y
sudo apt update
sudo apt install python3.6-dev python3.6-venv -y
python3.6 -m venv env

source env/bin/activate
python -m pip install -r requirements.txt
