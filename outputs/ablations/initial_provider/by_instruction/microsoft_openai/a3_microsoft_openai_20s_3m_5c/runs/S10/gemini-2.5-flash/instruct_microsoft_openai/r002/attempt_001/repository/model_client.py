import os
import openai

def get_openai_client() -> openai.OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    api_base = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    return openai.OpenAI(
        api_key=api_key,
        base_url=api_base,
    )

