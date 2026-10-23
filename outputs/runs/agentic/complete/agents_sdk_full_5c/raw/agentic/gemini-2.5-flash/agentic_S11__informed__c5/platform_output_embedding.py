import os
import cohere # Cohere SDK
from typing import List

def embed_platform_output(text_to_embed: str, model_id: str = "embed-english-v3.0") -> List[float]:
    api_key = os.environ.get("COHERE_API_KEY") # Provider-specific environment variable

    if not api_key:
        print("Please set the COHERE_API_KEY environment variable.")
        return []

    co = cohere.Client(api_key) # Provider-specific client

    try:
        response = co.embed(
            texts=[text_to_embed],
            model=model_id, # Provider-specific model ID
            input_type="clustering" # Example input type
        )
        # The embedding is usually the first (and only) item in the embeddings list
        return response.embeddings[0]
    except cohere.core.CohereError as e:
        print(f"Error generating embedding with Cohere: {e}")
        return []

if __name__ == '__main__':
    output_text = "This is a sample sentence for embedding."
    embedding_model = "embed-english-v3.0" # Cohere's latest English embedding model

    print(f"Generating embedding for: '{output_text}' using Cohere '{embedding_model}'...")
    embedding = embed_platform_output(output_text, embedding_model)

    if embedding:
        print(f"Embedding (first 5 dimensions): {embedding[:5]}...")
        print(f"Embedding dimension: {len(embedding)}")
    else:
        print("Failed to generate embedding.")
