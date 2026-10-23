import os
from openai import OpenAI

def stream_platform_generation(prompt: str, model_name: str = "gpt-4"):
    """
    Streams output from a managed model platform while preserving provider response objects.
    """
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url=os.environ.get("OPENAI_API_BASE", "https://api.openai.com/v1")
    )
    
    stream = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    
    for chunk in stream:
        yield chunk
