from wit import Wit
import json
import re
from tools.places import query_loc, directions
from tools.email_reminder import text_send, email_send

w = Wit('KL2CAZCLTOXH2DWULLZF7J5SCKLLN4IL')
maps_key = open('keys/places.key.txt', 'r').read()
geo_key = open('keys/geocode.key.txt', 'r').read()

print("[Hello!]: Hello!")
chatting = True
while chatting:
    usr_input = input(":::: ")

    if (usr_input == "q"):
        chatting = False
    else:
        print("Contacting wit.ai ...")
        response = w.get_message(usr_input)
        for entity in response["outcomes"][0]['entities']:
            if entity == "local_search_query":
                search_query = response["outcomes"][0]['entities'][entity][0]["value"]
                search_results = query_loc(search_query, maps_key, 5)
                print("There was more than one {} near you.".format(search_query))
                for i in range(len(search_results)):
                    print(search_results[i][0][0])
                print("Would you like me to send directions to {}?".format(search_results[0][0][0]))
                usr_input = input(":::: ")
                response = w.get_message(usr_input)
                for entity in response["outcomes"][0]['entities']:
                    print(response["outcomes"][0]['entities'][entity][0]["value"])
                    if response["outcomes"][0]['entities'][entity][0]["value"] == "affirmative":
                        res = directions(geo_key, search_results[0][0][1])
                        print("Ok, here are the directions:")
                        for i in res[0]['legs'][0]['steps']:
                            print(re.sub(r'<.*?>', '', i['html_instructions']))
                    else:
                        print("Ok no problem!")
            elif entity == "reminder":
                reminder = response["outcomes"][0]['entities'][entity][0]["value"]
                print("When would you like me to remind you of that?")
                usr_input = input(":::: ")
                response = w.get_message(usr_input)
                for entity in response["outcomes"][0]['entities']:
                    if entity == "duration":
                        t = response["outcomes"][0]['entities'][entity][0]['normalized']['value']
                    else:
                        print("I'm sorry, I didn't understand that time phrase. Please input in a more normal format ya dingus.")
                        pass
                print("And would you like me to do that via messaging or email?")
                usr_input = input(":::: ")
                if usr_input == "text":
                    text_send(reminder, t)
                else:
                    print("And what email should I send that to?")
                    email = input(":::: ")
                    email_send(email, reminder, t)
