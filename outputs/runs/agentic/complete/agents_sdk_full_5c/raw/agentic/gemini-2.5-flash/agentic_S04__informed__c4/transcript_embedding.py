import os
import openai
from typing import List

def get_text_embedding(text: str) -> List[float] | None:
    """Generates a text embedding for a given text segment using OpenAI Embeddings (text-embedding-ada-002)."""
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    try:
        print(f"Generating embedding for text (first 50 chars): '{text[:50]}...'")
        response = openai.embeddings.create(
            input=[text],
            model="text-embedding-ada-002"
        )
        embedding = response.data[0].embedding
        print(f"Embedding generated. Dimension: {len(embedding)}")
        return embedding
    except Exception as e:
        print(f"Error generating embedding with OpenAI: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    # Ensure OPENAI_API_KEY is set in your environment
    sample_transcript_segment = "The quick brown fox jumps over the lazy dog. This is a sentence for embedding."
    # embedding_vector = get_text_embedding(sample_transcript_segment)
    # if embedding_vector:
    #     print("\nGenerated Embedding (first 5 values):")
    #     print(embedding_vector[:5])
    pass
