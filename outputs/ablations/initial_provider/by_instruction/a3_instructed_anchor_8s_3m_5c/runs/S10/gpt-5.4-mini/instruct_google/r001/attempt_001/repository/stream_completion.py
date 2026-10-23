import os

from google import genai

from model_client import default_config


def stream_completion(prompt: str):
    config = default_config()
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    for chunk in client.models.generate_content_stream(model=config.model, contents=prompt):
        if getattr(chunk, "text", None):
            yield chunk.text
