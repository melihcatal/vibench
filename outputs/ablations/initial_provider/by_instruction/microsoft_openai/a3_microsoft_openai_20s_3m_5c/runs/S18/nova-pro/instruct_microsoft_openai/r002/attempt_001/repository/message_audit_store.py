import openai

def store_message(message):
    client = openai.Client()
    client.store(message)