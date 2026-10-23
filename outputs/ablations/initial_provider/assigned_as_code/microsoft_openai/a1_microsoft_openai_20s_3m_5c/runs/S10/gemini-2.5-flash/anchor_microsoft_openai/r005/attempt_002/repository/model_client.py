import os
from openai import OpenAI

def get_openai_client(api_key: str = None):
    return OpenAI(api_key=api_key or os.environ.get('OPENAI_API_KEY'))
