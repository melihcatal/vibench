import os
import cohere
from dotenv import load_dotenv

from speech_models import EmbeddingResponse

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")


def embed_caption_chunk(text_chunk: str) -> EmbeddingResponse:
    """Generates an embedding for a text chunk using Cohere."""
    if not COHERE_API_KEY:
        raise ValueError("COHERE_API_KEY is not configured in environment.")

    co = cohere.Client(COHERE_API_KEY)

    response = co.embed(
        texts=[text_chunk], model="embed-english-v3.0", input_type="search_document"
    )

    embedding = response.embeddings[0]

    return EmbeddingResponse(embedding=embedding)


if __name__ == "__main__":
    caption = "The new feature will be deployed next Tuesday."
    embedding_response = embed_caption_chunk(caption)

    print(f"Text: {caption}")
    # Print first 5 dimensions of the embedding for brevity
    print(f"Embedding (first 5 dims): {embedding_response.embedding[:5]}")
    print(f"Total embedding dimensions: {len(embedding_response.embedding)}")
