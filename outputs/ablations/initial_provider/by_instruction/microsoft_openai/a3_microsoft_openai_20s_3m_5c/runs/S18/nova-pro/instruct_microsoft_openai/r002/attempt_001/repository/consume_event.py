import openai

def consume_event():
    client = openai.Client()
    message = client.consume()
    return message