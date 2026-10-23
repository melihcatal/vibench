import openai

def check_safety(message):
    client = openai.Client()
    return client.check_safety(message)