import requests
import json
from geopy.distance import vincenty
from googlemaps import Client
from datetime import datetime

#key = open('keys/places.key.txt', 'r').read()

def get_location():
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    return lat, lon

def query_loc(query, key, n=10):
    lat, lon = get_location()
    gmaps = Client(key)

    local = gmaps.places(query, (lat, lon))

    l = list(([x['name'], x['formatted_address']], vincenty((x['geometry']['location']['lat'], x['geometry']['location']['lng']),
                           (lat, lon))) for x in local['results'])
    sl = sorted(l, key=lambda x: x[1].miles)

    return sl[:n]

def directions(key, address, mode="transit"):
    lat, lon = get_location()
    gmaps = Client(key)
    reverse_geocode_result = gmaps.reverse_geocode((lat, lon))[0]['formatted_address']
    print(reverse_geocode_result, address)
    now = datetime.now()
    directions_result = gmaps.directions(reverse_geocode_result,
                                     address,
                                     mode,
                                     departure_time=now)
    return directions_result
