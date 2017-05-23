import sys
from wit import Wit
from datetime import datetime

sys.path.insert(0, '~/Desktop/Programming/Work/Hello/tools/')
from tools.places import query_loc, directions
from tools.email_reminder import text_send, email_send

if len(sys.argv) != 2:
    print('usage: python ' + sys.argv[0] + ' <wit-token>')
    exit(1)
access_token = sys.argv[1]

# Quickstart example
# See https://wit.ai/ar7hur/Quickstart
# Full run command: python alt_main.py 2CCTOZRLLGMPT3L6A3VEFRMAX6QKFBPT

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
    key = open('keys/places.key.txt', 'r').read()
    context = request['context']
    print(context['location'])
    print(directions(key, context['location']))
    print("Let me know if I can help you with anything else.")
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

actions = {
    'send': send,
    'update_location': update_location,
    'send_location': send_location,
    'process_yesno': process_yesno,
    'send_directions': send_directions,
    'store_remind_message': store_remind_message,
    'send_remind_message': send_remind_message
}

client = Wit(access_token=access_token, actions=actions)
client.interactive()
