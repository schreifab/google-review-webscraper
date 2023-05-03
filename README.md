# google-review-webscraper
This Repository contains an experimental version of a google review webscraper developed during a university project.
It scrapes review data from google maps for a list of given locations and writes them as json and geojson. It is designed for acedemical usage. 

**Important:** That is an experimatel version wich still has some issues. I do not take responsibility for the correctness of the results.
Feel free to make improvements.

## Usage-Guidline

1. Create an python environment. Install Selenium, Beautiful Soap and geopy.
2. Install a Google Chrome driver according to your Google Chrome version.
3. Create or edit the enviroment variable "path". Copy your driver to the set path. Change the path in line 20 of the python code (driver = ).
4. Generate or write a list of all locations from which you want to scrape the data. Split the locations by ; (like in locations.txt). Save the data under locations.txt or change the path in line 23 (location_file = ).
5. Optional: Modify the output files (line 21 and 23).
6. Run the webscraper. A Chrome tab will be opend. After that, to avoid problems: **Move the coursor to the left side of the tab (where the reviews are diplayed). Don't move the coursor during running the code.**
7. If the webscraper stopped (e.g. lost connection): In the python console, the last iteration step is output. Change i in line 60 to the given value and restart to continue.
8. After the script is finished: Open the geojson file. Write 

{"type": "FeatureCollection", "comment": "test", "features": [

before the first line. 
Replace the last , through ]}

9. Open QGIS. Add the results as Vector Layer. If every thing worked out, you could watch the results on map. 

## Known Issues/ Things to do:
1. The programm currently skips the location, if more that one location is found for the name. For automatic generated location names, this means some of the locatiosn in the list are not scraped.
2. The Script generates the geotag from the adress using nominator. This does not allways work, so arround 5% have no geotag. Those are displayed on Null Island (Means they have the coordiantes 0,0 for identfification). Obviously it would be much better to get the coordinates directly from Google Maps. However, I didn't fount a good solution to do so yet. 
3. The program is very slow. This is because you always have to wait until the results of the page are loaded (isnespecially when scrolling). It is recommended to let the program run overnight.
4. It might happend, that Google changes his Website style and classes. In this case everything must be revised.
