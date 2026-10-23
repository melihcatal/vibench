import os
from google import genai


def embed_ocr_sections(sections):
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY", ""))
    model = "gemini-embedding-001"
    texts = [
        section if isinstance(section, str) else str(section) for section in sections
    ]
    response = client.models.embed_content(model=model, contents=texts)
    return response.embeddings
