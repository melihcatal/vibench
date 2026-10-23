import openai

def translate_payload(message):
    client = openai.Client()
    return client.translate(message)