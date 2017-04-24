class Conversation(object):
    def __init__(self, access_token):
        try:
            self.w = Wit(access_token)
        except:
            print("Error: Incorrect access token passed, please make sure you have the correct access token."

    def text_response(input):
        chatting = True

        if input == 'q' or input == 'quit':
            chatting = False

