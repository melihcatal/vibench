from google import genai

from embeddings_client import get_google_client


def retrieval_audio_brief(results) -> str:
    client = get_google_client()
    prompt = f"Create a short spoken brief from these retrieved search results: {results}"
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)
    return response.text
