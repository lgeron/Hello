import sys, pickle, re
from wit import Wit
from datetime import datetime

sys.path.insert(0, '~/path/to/Hello/tools/')
from tools.places import query_loc, directions
from tools.email_reminder import text_send, email_send
from tools.find_sim_to_query import search_query

if len(sys.argv) != 2:
    print('usage: python ' + sys.argv[0] + ' <wit-token>')
    exit(1)
access_token = sys.argv[1]

texts = pickle.load(open('texts.p', 'rb'))

# Quickstart example
# See https://wit.ai/ar7hur/Quickstart
# Full run command: python alt_main.py 2CCTOZRLLGMPT3L6A3VEFRMAX6QKFBPT
# TODO: Email reminders need to be hosted on a server
# TODO: Handle out of story solutions

def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val

def send(request, response):
    print(response['text'])

def update_location(request):
    context = request['context']
    entities = request['entities']

    context['local_search_query'] = entities['local_search_query'][0]['value']
    return context

def send_location(request):
    key = open('keys/places.key.txt', 'r').read()
    context = request['context']

    locations = query_loc(context['local_search_query'], key, n=1)
    context['location'] = locations[0][0][1]
    print("I've found the nearest {} to you:".format(context['local_search_query']))
    for l in locations[0][0]:
        print(l)
    print("Distance is {}".format(locations[0][1]))
    return context

def process_yesno(request):
    context = request['context']
    entities = request['entities']
    context['yesno'] = entities['yesno'][0]['value']

    return context

def send_directions(request):
    key = open('keys/geocode.key.txt', 'r').read()
    context = request['context']
    try:
        loc = context['location']
    except KeyError:
        print("I'm sorry, I'm not sure where you would like to go. Please search for a location first before asking for directions.")
        return context
    if not isinstance(context['location'], unicode):
        loc = context['location'][-1]
    directions_result = directions(key, loc)
    for step in directions_result[0]['legs'][0]['steps']:
        if 'steps' in step:
            print(re.sub('<.*?>', '', step['steps'][0]['html_instructions']))
        else:
            print(re.sub('<.*?>', '', step['html_instructions']))
    if 'arrival_time' in directions_result[0]['legs'][0]:
        arrival_time = directions_result[0]['legs'][0]['arrival_time']
        print("Estimated arrival time: {0} {1}".format(arrival_time['text'], arrival_time['time_zone']))
    print("Let me know if I can help you with anything else.")
    del context['location']
    return context

def store_remind_message(request):
    context = request['context']
    entities = request['entities']
    context['remind_message'] = entities['remind_message'][0]['value']
    context['time_to_reminder'] = entities['datetime'][0]['value']

    return context

def send_remind_message(request):
    context = request['context']
    time = context['time_to_reminder']
    remind_message = context['remind_message']

    text_send(remind_message, time)
    del context['time']
    del context['remind_message']
    return context

def process_query(request):
    context = request['context']
    entities = request['entities']

    query = [entities['query'][0]['value']]
    text = search_query(query, texts, 5)
    for t in text:
        print(t)
    return context


actions = {
    'send': send,
    'update_location': update_location,
    'send_location': send_location,
    'process_yesno': process_yesno,
    'send_directions': send_directions,
    'store_remind_message': store_remind_message,
    'send_remind_message': send_remind_message,
    'process_query': process_query
}

client = Wit(access_token=access_token, actions=actions)
client.interactive()
