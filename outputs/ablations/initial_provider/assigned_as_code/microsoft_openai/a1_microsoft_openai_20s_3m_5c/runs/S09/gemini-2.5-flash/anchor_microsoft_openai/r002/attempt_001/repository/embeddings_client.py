import os
from openai import OpenAI


def get_openai_client(api_key=None):
    api_key = api_key or os.environ.get('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OpenAI API key not found. Please set OPENAI_API_KEY environment variable or pass it directly.")
    return OpenAI(api_key=api_key)
