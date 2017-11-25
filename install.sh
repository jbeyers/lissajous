#!/bin/bash
virtualenv ve --python=python3.6
. ve/bin/activate
pip install --upgrade pip
pip install -r requirements.txt 
jupyter nbextension enable --py --sys-prefix widgetsnbextension
deactivate
