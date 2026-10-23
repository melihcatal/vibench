from google import genai

from embeddings_client import get_google_client


def corpus_safety(text: str) -> bool:
    client = get_google_client()
    response = client.models.generate_content(model="gemini-2.0-flash", contents=f"Check whether this text is safe to embed and return only yes or no: {text}")
    return "yes" in response.text.lower()
