from wit import Wit
import json
from tools.places import query_loc

w = Wit('KL2CAZCLTOXH2DWULLZF7J5SCKLLN4IL')

print("[Hello!]: Hello!")
chatting = True
while chatting:
	usr_input = input(":::: ")

	if (usr_input == "q"):
		chatting = False
	else:
		print("Contacting wit.ai ...")
		response = w.get_message(usr_input)
		print(response)
		for entity in response["outcomes"][0]['entities']:
			if (entity == "local_search_query"):
				search_query = response["outcomes"][0]['entities'][entity][0]["value"]
				search_results = query_loc(search_query, "GOOGLE_MAPS_KEY", 5)
