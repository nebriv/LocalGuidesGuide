import time
import googlemaps
from datetime import datetime
import configparser
import os
from bs4 import BeautifulSoup

def find_in(place_id, parsed_list):
    for each in parsed_list:
        if place_id == each['place_id']:
            return True
    return False

def main():
    if not os.path.exists("settings.conf"):
        print("Missing settings.conf file, make sure you create a new file from settings.conf.example and fill in the settings")

    parser = configparser.ConfigParser()
    parser.read('settings.conf')
    settings = parser['Settings']
    g_api_key = settings.get('google_api_key', None)
    center_lat_long = settings.get('center_lat_lon', None)
    radius = settings.getint('radius')

    max_places = settings.getint('max_places', 50)

    location_types = settings.get('location_types', None)
    location_types = location_types.split(",")

    generation_settings = parser['DirectionGeneration']
    transport_mode = generation_settings.get('transportation_mode', 'walking')
    starting_location = generation_settings.get('starting_location', None)
    generate_directions = generation_settings.getboolean('enabled', False)

    if len(location_types) == 0:
        print("Missing location types")
        exit()

    if "," not in center_lat_long:
        print("Missing or improper formatt for lat lon. Must be 00.00,00.00")
        exit()

    if transport_mode not in ['walking', 'driving', 'bicycling', 'transit']:
        print("Invalid transport mode: %s. Must be walking, driving, bicycling, or transit." % transport_mode)
        exit()

    if radius <= 0 or radius >= 15000:
        print("Invalid radius, must be greater than 0 and less than 15000")
        exit()

    if starting_location == None:
        print("Missing starting location.")
        exit()

    gmaps = googlemaps.Client(key=g_api_key)


    parsed_results = []
    results = []

    types = location_types

    for type in types:
        print("Searching Google for %ss near you" % type)
        search = gmaps.places_nearby(location=center_lat_long, type="%s" % type, radius=radius)

        results += search['results']

        while "next_page_token" in search:
            time.sleep(2)
            search = gmaps.places_nearby(page_token=search['next_page_token'])
            print("Next Page Token Found... Collecting Results")
            results += search['results']
            time.sleep(2)

    print("Found %s nearby places:" % len(results))

    for place in results:
        if "establishment" in place['types'] and "permanently_closed" not in place:

            if not find_in(place['place_id'], parsed_results):

                print("Getting details for %s" % place['name'])
                details = gmaps.place(place['place_id'], fields=["formatted_address","geometry","permanently_closed","name","place_id","url","photo"])['result']
                place_dict = {"name": place['name'],
                              "type": place['types'],
                              "place_id": place['place_id'],
                              "lat": place['geometry']['location']['lat'],
                              "lng": place['geometry']['location']['lng'],
                              "results": place,
                              "details": details}

                if "formatted_address" in details:
                    place_dict['address'] = details['formatted_address']
                else:
                    place_dict['address'] = "Unknown"

                if "opening_hours" in place:
                    place_dict['has_hours'] = True
                else:
                    place_dict['has_hours'] = False

                if "rating" in place:
                    place_dict['has_rating'] = True
                else:
                    place_dict['has_rating'] = False

                if "photos" in details:
                    place_dict['has_photo'] = len(details['photos'])
                else:
                    place_dict['has_photo'] = 0

                if "permanently_closed" in place:
                    place_dict['permanently_closed'] = True
                else:
                    place_dict['permanently_closed'] = False

                if "reviews" in details:
                    place_dict['has_reviews'] = len(details['reviews'])
                else:
                    place_dict['has_reviews'] = "N/A"

                if "url" in details:
                    place_dict['url'] = details['url']
                else:
                    place_dict['url'] = False


                parsed_results.append(place_dict)
            else:
                print("Already parsed! %s" % place_dict['name'])

    directions_list = []
    places = []
    print()
    print("Results:")

    for place_dict in parsed_results:
        if place_dict['has_photo'] == 0:
            print("%s - %s" % (place_dict['name'], place_dict['address']))
            print("   Type: %s" % place_dict['type'])
            print("   Has Hours: %s" % place_dict['has_hours'])
            print("   Photos: %s" % place_dict['has_photo'])
            print("   Reviews: %s" % place_dict['has_reviews'])
            print("   Has Rating: %s" % place_dict['has_rating'])
            print("   URL: %s" % place_dict['url'])

            directions_list.append(place_dict['address'])
            places.append(place_dict)
            if len(parsed_results) == max_places:
                print("Max place threshold from settings reached, stopping!")
                break

    if not generate_directions:
        print("Direction instructions disabled, exiting")
        exit()

    print("Calculating directions to places without photos")
    now = datetime.now()
    directions_result = gmaps.directions(origin=starting_location, destination=starting_location, waypoints=directions_list, mode=transport_mode, departure_time=now, optimize_waypoints=True)

    total_distance = 0
    for i, each in enumerate(directions_result[0]['legs']):

        total_distance += each['distance']['value']
        print(places[i]['name'])
        print("Destination: %s" % each['end_address'])
        print("Distance: %s" % each['distance']['text'])
        print("Directions: %s" % BeautifulSoup(each['steps'][0]['html_instructions']).get_text())
        print("")

    print("Total Distance: %sm" % total_distance)

if __name__ == '__main__':
    main()




