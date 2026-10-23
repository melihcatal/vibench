from google import genai

from embeddings_client import get_client


def corpus_safety(payload, config=None):
    config = config or {}
    with get_client(config) as client:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=payload["text"])
    return {"safe": "unsafe" not in response.text.lower(), "analysis": response.text}
