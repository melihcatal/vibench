import openai

def summarize_messages(messages):
    client = openai.Client()
    summaries = [client.summarize(message) for message in messages]
    return summaries