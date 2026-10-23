import os
from openai import OpenAI


def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    return OpenAI(api_key=api_key)
