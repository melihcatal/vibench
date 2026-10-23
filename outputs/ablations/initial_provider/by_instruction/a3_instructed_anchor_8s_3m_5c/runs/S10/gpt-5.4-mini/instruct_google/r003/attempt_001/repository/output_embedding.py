import os

from google import genai


def embed_output(text: str):
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    response = client.models.embed_content(
        model=os.getenv("GOOGLE_GENAI_EMBEDDING_MODEL", "text-embedding-004"),
        contents=text,
    )
    return getattr(response, "embeddings", response)
