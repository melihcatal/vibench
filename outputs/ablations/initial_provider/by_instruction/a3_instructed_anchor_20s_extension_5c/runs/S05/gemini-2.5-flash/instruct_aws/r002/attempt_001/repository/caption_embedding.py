
import os
import cohere

COHERE_API_KEY = os.environ.get("COHERE_API_KEY")
COHERE_EMBED_MODEL = os.environ.get("COHERE_EMBED_MODEL", "embed-english-v3.0")

async def embed_caption_chunks(caption_chunks: list[str]) -> list[list[float]]:
    """
    Embeds caption chunks for semantic meeting search using Cohere Embed API.
    """
    if not COHERE_API_KEY:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(COHERE_API_KEY)

    try:
        # Cohere's embed takes a list of texts
        response = co.embed(
            texts=caption_chunks,
            model=COHERE_EMBED_MODEL,
            input_type="search_document" # Or "search_query", "classification", "clustering" depending on use case
        )
        return response.embeddings
    except Exception as e:
        print(f"Error embedding with Cohere: {e}")
        return []
