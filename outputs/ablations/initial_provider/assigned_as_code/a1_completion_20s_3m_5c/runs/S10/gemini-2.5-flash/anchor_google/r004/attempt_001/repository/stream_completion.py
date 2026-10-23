import os
from google import genai
from model_client import get_gemini_client

def stream_completion(payload, config=None):
    config = config or {}
    text = payload["text"]

    client = get_gemini_client(api_key=config.get("api_key"))
    responses = client.models.generate_content(model="gemini-2.5-flash", contents=text, stream=True)

    streamed_output = []
    for chunk in responses:
        streamed_output.append(chunk.text)
    return {"streamed_text": "".join(streamed_output)}
