import os
from model_client import get_client

def stream_platform_generation(prompt: str):
    client = get_client()
    return client.chat.completions.create(model=os.getenv('OPENAI_MODEL', 'gpt-4.1-mini'), messages=[{'role': 'user', 'content': prompt}], stream=True)
