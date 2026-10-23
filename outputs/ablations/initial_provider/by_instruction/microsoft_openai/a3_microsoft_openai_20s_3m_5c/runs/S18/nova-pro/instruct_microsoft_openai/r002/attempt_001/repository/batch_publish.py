import openai

def batch_publish(messages):
    client = openai.Client()
    response = client.batch_publish(messages)
    return response