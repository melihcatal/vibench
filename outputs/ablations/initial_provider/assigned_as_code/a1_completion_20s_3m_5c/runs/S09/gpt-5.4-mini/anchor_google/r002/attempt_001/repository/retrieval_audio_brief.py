from google import genai

from embeddings_client import get_client


def retrieval_audio_brief(payload, config=None):
    config = config or {}
    brief_prompt = payload["results"]
    with get_client(config) as client:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=brief_prompt)
    return {"brief_text": response.text}
