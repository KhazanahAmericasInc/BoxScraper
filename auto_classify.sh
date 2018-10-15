#!/bin/bash

#
#
#
# This script auto-scrapes the box repository, classifies the images
# and returns an ouput of the neural net of the box repository
#
#
#

python3 box_scrape.py
python3 cnn_v2.py 
rm net_output.txt
