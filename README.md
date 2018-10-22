# BoxScraper
Scrapes images off of box and writes it to a local directory. Also includes a simple box filename parser and map plotter. Plots a heatmap for the traffic events tracked. Plots red markers for the timber trucks detected. Designed to be used in conjunction with the sensortower.

## Installation
Install Python 3 and the following Python 3 dependencies:
- Tensorflow
- OpenCV
- Numpy
- boxsdk
- webbot
- configparser
- gmplot

And fill in config.ini with information from the Box account (See Evernote) - TrafficClient app.

## Quickstart Guide
After following the instructions in the *installation* section:
1. give executable permission to auto_map_classify.sh by typing the following in the terminal
```
chmod u+x auto_map_classify.sh
```
2. run auto_map_classify.sh by typing the following in the terminal
```
./auto_map_classify.sh
```
3. the data markers will be plotted on the map.


## Contents
#### Bash Scripts
| Script Name | Description |
|:------------|:------------|
|auto_map_classify.sh| Automatically scrapes Box, classifies the images, and parses the data to be plotted onto a map|
|auto_classify.sh| Automatically scrapes Box, and classifies the images, outputting the results to net_output.txt|
|clean.sh| Cleans the downloaded images and the cnn output|

#### Python Scripts
| Script Name | Description |
|:------------|:------------|
|box_scrape.py| Scrapes all images from Box, skipping the already-downloaded images. Places images into '/BoxScraper/downloads/'|
|cnn_v2.py| Classifies images from '/BoxScraper/downloads/*' and outputs to /BoxScraper/net_output.txt|
|analyze_data.py|parses filenames to JSON and plots data onto a google map. Outputs the map to /BoxScraper/map.html|





