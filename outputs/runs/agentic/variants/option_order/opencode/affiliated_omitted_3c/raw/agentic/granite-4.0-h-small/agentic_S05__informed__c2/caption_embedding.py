import asyncio
from google.cloud import genai

# Google Gemini Embeddings SDK import identifies the provider


async def embed_captions(caption_chunks):
    """Embed live caption chunks for semantic search using Gemini."""
    client = genai.Client()  # Uses GOOGLE_API_KEY env var
    model = "gemini-1.5-pro"  # Example embedding-capable model
    embeddings = client.embeddings(model=model)
    for chunk in caption_chunks:
        response = embeddings.embed_content(content=chunk)
        yield {
            "chunk": chunk,
            "embedding": response.data[0].embedding.values,
        }
