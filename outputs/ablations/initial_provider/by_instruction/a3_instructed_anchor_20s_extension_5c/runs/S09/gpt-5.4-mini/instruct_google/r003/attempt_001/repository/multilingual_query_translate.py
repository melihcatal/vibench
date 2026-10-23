from google import genai

from embeddings_client import get_google_client


def multilingual_query_translate(query: str, target_language: str = "en") -> str:
    client = get_google_client()
    prompt = f"Translate this query to {target_language} and return only the translation: {query}"
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    return response.text.strip()
