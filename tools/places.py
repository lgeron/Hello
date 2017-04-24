import argparse
import requests
import json
import pickle
import operator
from geopy.distance import vincenty
from googlemaps import Client

def handle_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--access_token', help='file containing the access token', default='access_token.txt')
    parser.add_argument('-q', '--query', help='string to query location services with')
    parser.add_argument('-r', '--radius', help='radius around which to look', default=50) 
    parser.add_argument('-n', '--num_res', help='number of results to keep', default=10)
    parser.add_argument('-o', '--outfile', help='file to write results to', default='place.p')

    return vars(parser.parse_args())

args = handle_args()
key = open(args['access_token'], 'r').read()

def get_location():
    send_url = 'http://freegeoip.net/json'
    r = requests.get(send_url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    return lat, lon

lat, lon = get_location()

gmaps = Client(key)

local = gmaps.places(args['query'], (lat, lon))

l = list(([x['name'], x['formatted_address']], vincenty((x['geometry']['location']['lat'], x['geometry']['location']['lng']),
                           (lat, lon))) for x in local['results'])
sl = sorted(l, key=lambda x: x[1].miles)
print(sl)


pickle.dump(sl[:int(args['num_res'])], open(args['outfile'], 'wb'))
