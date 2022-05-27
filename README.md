# Local Guide's Guide

A quick script to find nearby businesses or places on Google Maps that do not have any photos (It'll also list out if theres any hours listed, reviews, etc) . Generates a list and can generate directions to each location and back to the starting location. This has been a bit superseded by Google's "Contribute" button, but hey, might be useful for someone.

Caution - this does use Google's Map API and can quickly incur some cost especially for generating lots of directions.

Example Output:

![image](https://user-images.githubusercontent.com/1825214/170608728-f3dba54c-ed8c-4e11-a9b4-cf71b28e8f64.png)

![image](https://user-images.githubusercontent.com/1825214/170608813-525bbbb7-c806-44e1-93c8-e8b901f01037.png)

![image](https://user-images.githubusercontent.com/1825214/170608830-33506bfe-44e1-4a46-ae9e-4e7267522fdb.png)


## Installation
1. pip install -r requirements
2. Get a valid google maps API key for Google maps: https://developers.google.com/maps/documentation/directions/get-api-key

## Usage
1. Copy the settings.conf.example file to settings.conf
2. Fill in the appropriate variables
3. Run main.py
