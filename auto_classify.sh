#!/bin/bash

#
#
#
# This script auto-scrapes the box repository, classifies the images
# and returns an ouput of the neural net of the box repository
#
#
#

# Scrape box
python3 box_scrape.py
# Filter out all images except car images
python3 classify_image.py --image_file "./downloads/"
# Classify car images
python3 cnn_v2.py 
