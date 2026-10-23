import os
import openai

def get_openai_embedding_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    return openai.OpenAI(api_key=api_key)

OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"
