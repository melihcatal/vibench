import os
from openai import OpenAI


def get_openai_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def default_model():
    return os.getenv("OPENAI_MODEL", "openai/gpt-5.4-mini")
