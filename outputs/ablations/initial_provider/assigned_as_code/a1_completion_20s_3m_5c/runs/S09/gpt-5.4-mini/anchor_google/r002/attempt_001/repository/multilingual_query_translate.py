from google import genai

from embeddings_client import get_client


def multilingual_query_translate(payload, config=None):
    config = config or {}
    target_language = payload.get("target_language", "English")
    prompt = f'Translate this query to {target_language}: {payload["query"]}'
    with get_client(config) as client:
        response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    return {"translated_query": response.text}
