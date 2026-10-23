import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def moderate_claims(claims):
    response = openai.Moderation.create(input=claims)
    return response
