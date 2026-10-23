import os
import cohere
from speech_models import EmbeddingResponse


def embed_caption_chunk(caption_chunks: list[str]) -> EmbeddingResponse | None:
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")

    co = cohere.Client(api_key)

    if not caption_chunks:
        return None

    try:
        response = co.embed(
            texts=caption_chunks,
            model="embed-english-v3.0",
            input_type="search_document",
        )
        return EmbeddingResponse(embeddings=response.embeddings)
    except cohere.CohereError as e:
        print(f"Cohere API error during embedding: {e}")
        return None
