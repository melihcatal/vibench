import os
import cohere
from document_models import EmbeddingResult


def embed_document_section(
    text: str, model: str = "embed-english-v3.0"
) -> EmbeddingResult:
    """Embed extracted document sections for semantic retrieval using Cohere Embed API."""
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("Please set COHERE_API_KEY environment variable")

    co = cohere.Client(api_key)

    response = co.embed(texts=[text], model=model, input_type="search_document")

    embedding = response.embeddings[0]

    return EmbeddingResult(
        embedding=embedding,
        model=model,
        text=text,
        token_count=response.meta.get("tokens", {}).get("total_tokens"),
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python ocr_embedding.py <text> [model]")
        print(
            "Example: python ocr_embedding.py 'Invoice for services rendered' embed-english-v3.0"
        )
        sys.exit(1)

    text = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) > 2 else "embed-english-v3.0"

    result = embed_document_section(text, model)

    print(f"Embedding generated using model: {result.model}")
    print(f"Text: {result.text}")
    print(f"Embedding dimensions: {len(result.embedding)}")
    print(f"First 5 values: {result.embedding[:5]}")
    if result.token_count:
        print(f"Token count: {result.token_count}")
