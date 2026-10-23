from openai import OpenAI
import os

def get_openai_client():
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
