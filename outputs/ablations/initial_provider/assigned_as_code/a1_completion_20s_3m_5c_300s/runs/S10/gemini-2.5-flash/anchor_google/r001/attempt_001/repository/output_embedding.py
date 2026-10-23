import os

from google import genai

def embed_output(payload, config=None):
    config = config or {}
    with genai.Client(api_key=config.get("api_key") or os.environ["GOOGLE_API_KEY"]) as client:
        # The genai library provides embedding functionality.
        # We'll use the embedding model available through the genai client.
        # The model name for embedding is typically different from the text generation models.
        embedding_model = "embedding-001" # This is a common embedding model ID for Google Generative AI

        response = client.embed_content(
            model=embedding_model,
            content=payload["text"]
        )
    
    # The embedding is usually accessed via .embedding attribute of the response.
    embedding = response.embedding.values if response.embedding else []
    return {"embedding": embedding}
