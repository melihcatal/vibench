import openai

def dead_letter(message):
    client = openai.Client()
    client.dead_letter(message)