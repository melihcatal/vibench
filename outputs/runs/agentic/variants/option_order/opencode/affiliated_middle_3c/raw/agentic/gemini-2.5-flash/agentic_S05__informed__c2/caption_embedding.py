import os
import google.generativeai as genai


def embed_caption_chunk(caption_chunk: str) -> list[float]:
    """Embeds a single caption chunk using Google Gemini Embeddings."""
    # GOOGLE_API_KEY environment variable should be set.
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    try:
        response = genai.embed_content(
            model="models/embedding-001",
            content=caption_chunk,
            task_type="RETRIEVAL_DOCUMENT",
        )
        return response["embedding"]
    except Exception as e:
        print(f"Error embedding caption chunk with Gemini API: {e}")
        return []


def embed_caption_chunks(caption_chunks: list[str]) -> list[list[float]]:
    """Embeds multiple caption chunks using Google Gemini Embeddings."""
    embeddings = []
    for chunk in caption_chunks:
        embeddings.append(embed_caption_chunk(chunk))
    return embeddings
