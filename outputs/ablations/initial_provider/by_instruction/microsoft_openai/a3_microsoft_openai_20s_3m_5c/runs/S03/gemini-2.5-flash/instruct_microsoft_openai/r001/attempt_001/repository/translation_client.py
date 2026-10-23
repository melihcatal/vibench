import openai
import os

def get_openai_client():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1") # Default to OpenAI's official API base
    return openai
