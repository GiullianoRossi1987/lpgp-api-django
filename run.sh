#!/usr/bin/bash
if [ $1 == "-p" ]
then
    echo "Checking SSLSERVER package installed"
    pip3 install django-sslserver
fi
python3 manage.py runsslserver 8000
