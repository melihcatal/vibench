import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def get_client():
    return openai