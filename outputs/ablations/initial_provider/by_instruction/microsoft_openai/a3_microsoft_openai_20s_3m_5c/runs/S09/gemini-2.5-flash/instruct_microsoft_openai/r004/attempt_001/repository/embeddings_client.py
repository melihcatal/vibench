import openai
import os

def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    return openai.OpenAI(api_key=api_key)

def get_embedding_model_id():
    return "text-embedding-ada-002"
