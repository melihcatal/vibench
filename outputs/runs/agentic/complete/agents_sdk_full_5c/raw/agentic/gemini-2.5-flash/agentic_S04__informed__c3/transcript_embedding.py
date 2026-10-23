import os
import google.generativeai as genai
from typing import List
from speech_models import EmbeddingRequest

def get_text_embedding_gemini(request: EmbeddingRequest) -> List[float]:
    """
    Generates an embedding for a given text using Google Gemini Embeddings.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    # Use a specific embedding model
    # 'embedding-001' is suitable for text embeddings
    model = 'models/embedding-001'

    try:
        response = genai.embed_content(
            model=model,
            content=request.text,
            task_type="RETRIEVAL_DOCUMENT" # Specify task type for better embeddings
        )
        if response.embedding:
            return response.embedding
        else:
            return []
    except Exception as e:
        print(f"Error calling Google Gemini Embeddings API: {e}")
        raise

if __name__ == "__main__":
    # Example usage
    sample_segment = "The quick brown fox jumps over the lazy dog."

    if not os.getenv("GOOGLE_API_KEY"):
        print("Please set the GOOGLE_API_KEY environment variable.")
    else:
        embedding_request = EmbeddingRequest(text=sample_segment)
        try:
            embedding = get_text_embedding_gemini(embedding_request)
            print(f"Text: '{sample_segment}'")
            print(f"Embedding (first 5 dimensions): {embedding[:5]}...")
            print(f"Embedding length: {len(embedding)}")
        except ValueError as e:
            print(f"Configuration error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
