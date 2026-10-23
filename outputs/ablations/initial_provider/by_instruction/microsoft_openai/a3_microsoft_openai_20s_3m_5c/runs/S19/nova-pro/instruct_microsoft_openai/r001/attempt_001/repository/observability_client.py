import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def create_observability_client():
    return openai