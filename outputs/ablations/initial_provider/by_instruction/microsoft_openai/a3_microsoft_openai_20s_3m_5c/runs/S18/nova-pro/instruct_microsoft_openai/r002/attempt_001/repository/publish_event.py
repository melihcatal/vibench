import openai

def publish_event(event):
    client = openai.Client()
    response = client.publish(event)
    return response