import os

from google import genai


def embed_output(payload, config=None):
    config = config or {}
    prompt = payload["text"]
    with genai.Client(api_key=config.get("api_key") or os.environ["GOOGLE_API_KEY"]) as client:
        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
    return {"embedding": response.embedding or []}
