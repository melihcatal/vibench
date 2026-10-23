import os
from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = "text-embedding-3-small"

def get_client():
    return OpenAI(api_key=OPENAI_API_KEY)