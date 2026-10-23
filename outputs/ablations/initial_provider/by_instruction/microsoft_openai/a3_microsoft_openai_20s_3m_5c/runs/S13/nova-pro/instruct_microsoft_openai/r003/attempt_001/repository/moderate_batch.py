import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def moderate_batch(texts):
    responses = openai.Moderation.create(input=texts)
    return [response.results[0].flagged for response in responses]