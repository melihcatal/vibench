import google.generativeai as genai
import os


def embed_script(text, api_key=None):
    if not api_key:
        api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set or provided.")

    genai.configure(api_key=api_key)
    model = "models/embedding-001"
    response = genai.embed_content(model=model, content=text)
    return response["embedding"]
