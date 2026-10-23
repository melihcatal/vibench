import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def moderate_text(text):
    response = openai.Moderation.create(input=text)
    return response.results[0].flagged