#!/bin/bash


# active xamp
sudo /opt/lampp/xampp startmysql
sudo /opt/lampp/xampp startapache

# active venv
source venv/bin/activate

# run app
python -m streamlit run main.py 
