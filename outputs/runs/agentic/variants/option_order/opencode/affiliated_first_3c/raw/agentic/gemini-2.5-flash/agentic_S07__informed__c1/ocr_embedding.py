import os
from typing import List
from document_models import TextExtractionResult, EmbeddingResult
import google.generativeai as genai


def embed_text(text_to_embed: TextExtractionResult, api_key: str) -> EmbeddingResult:
    genai.configure(api_key=api_key)

    # Use a specific embedding model, e.g., "models/embedding-001"
    # Ensure the model is available and suitable for the task.
    # The model ID is provider-specific and identifiable.
    model_name = "models/embedding-001"

    # The embedding API expects a list of texts
    response = genai.embed_content(model=model_name, content=[text_to_embed.text])

    # The embedding is a list of floats
    embedding_vector = response["embeddings"][0]

    return EmbeddingResult(embedding=embedding_vector)


if __name__ == "main":
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

    if not GOOGLE_API_KEY:
        print("Please set GOOGLE_API_KEY environment variable.")
    else:
        sample_text = TextExtractionResult(
            text="This is a document section about product features."
        )
        embedding_result = embed_text(sample_text, GOOGLE_API_KEY)
        print(f"Text: {sample_text.text}")
        print("Embedding (first 5 dimensions):")
        print(embedding_result.embedding[:5])
        print(f"Embedding length: {len(embedding_result.embedding)}")
