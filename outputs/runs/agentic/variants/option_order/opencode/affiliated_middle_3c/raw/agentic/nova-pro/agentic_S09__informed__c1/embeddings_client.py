import os
from openai import OpenAI


def get_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_model():
    return "text-embedding-ada-002"
