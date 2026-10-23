import google.generativeai as genai
import os


def get_embedding(text: str) -> list[float]:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set.")
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("embedding-001")
    response = model.embed_content(content=text)
    return response["embedding"]
