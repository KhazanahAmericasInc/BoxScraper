#!/bin/bash

#
#
#
# This script auto-scrapes the box repository, classifies the images
# and returns an ouput of the neural net of the box repository; then
# maps out the data and opens the map on google-chrome
#
#

# Scrape Box
python3 box_scrape.py
# Filter out all images except car images
python3 classify_image.py --image_file "./downloads/"
# Classify car images
python3 cnn_v2.py 
# Parse filenames, to car types and plot on a map
python3 analyze_data.py
# open the map on google chrome
google-chrome map.html
# remove the output files of cnn_v2.py
rm net_output.txt