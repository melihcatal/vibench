import os
from google.generativeai import GenerativeModel


def embed_translation_memory(text):
    os.environ["GOOGLE_API_KEY"] = "your-api-key"
    model = GenerativeModel("gemini-pro")
    response = model.generate_content(
        f"Embed this translated segment for translation-memory search: {text}"
    )
    return response.text
