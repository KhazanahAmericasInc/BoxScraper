#!/bin/bash

#
#
#
# This script auto-scrapes the box repository, classifies the images
# and returns an ouput of the neural net of the box repository; then
# maps out the data and opens the map on google-chrome
#
#

python3 box_scrape.py
python3 cnn_v2.py 
python3 analyze_data.py
google-chrome map.html