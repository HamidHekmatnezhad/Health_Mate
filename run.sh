#!/bin/bash

# flush currently ip
sudo ip addr flush enp4s0

# set ip 192.168.2.50
sudo ip addr add 192.268.2.50/24 dev enp4s0
ifconifg | grep "192.168....."

# active xamp
sudo /opt/lampp/xampp startmysql
sudo /opt/lampp/xampp startapache

# active venv
source venv/bin/activate

# run app
python -m streamlit run main.py 
