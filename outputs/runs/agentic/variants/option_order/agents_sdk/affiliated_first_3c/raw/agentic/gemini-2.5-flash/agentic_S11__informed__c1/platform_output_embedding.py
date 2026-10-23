import os
import google.generativeai as genai
from typing import List, Dict, Any

def embed_platform_output(text: str) -> Dict[str, Any]:
    """Embeds platform outputs for evaluation or retrieval using Gemini Embeddings."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set.")

    genai.configure(api_key=api_key)

    # The embedding model name. Use a concrete model identifier.
    embedding_model = "models/embedding-001"

    response = genai.embed_content(
        model=embedding_model,
        content=text,
        task_type="RETRIEVAL_DOCUMENT" # or other appropriate task type
    )

    embedding = []
    if response and hasattr(response, 'embedding') and hasattr(response.embedding, 'values'):
        embedding = list(response.embedding.values)

    return {"embedding": embedding, "raw_response": response}

if __name__ == '__main__':
    # Example usage (set GOOGLE_API_KEY env var)
    # output_text = "This is a sample text to embed."
    # embedding_result = embed_platform_output(output_text)
    # print(f"Embedding dimension: {len(embedding_result.get("embedding"))}")
    # print(f"First 5 embedding values: {embedding_result.get("embedding")[:5]}")
    pass
