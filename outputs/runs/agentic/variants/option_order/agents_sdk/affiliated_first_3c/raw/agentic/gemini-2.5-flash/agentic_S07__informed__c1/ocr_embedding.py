import os
import google.generativeai as genai
from typing import List

def get_text_embedding_gemini(text: str) -> List[float]:
    """Generates a text embedding using Google's Gemini Embeddings model."""
    # Ensure your GOOGLE_API_KEY environment variable is set.
    # genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) # This is usually configured globally

    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    model = "models/embedding-001"

    # The embedding model can embed a list of texts, but we're sending a single one here.
    response = genai.embed_content(
        model=model,
        content=text,
        task_type="RETRIEVAL_DOCUMENT"
    )

    # The embedding is in response['embedding'] for a single content item.
    return response['embedding']

if __name__ == '__main__':
    TEXT_TO_EMBED = "The quick brown fox jumps over the lazy dog."

    # Set your Google API Key in environment variable, e.g.:
    # export GOOGLE_API_KEY="YOUR_API_KEY"
    # Make sure to install the SDK: pip install google-generativeai

    # try:
    #     # Initialize the generative AI client (usually done once at app startup)
    #     # For standalone script, we configure it here.
    #     genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    #     embedding = get_text_embedding_gemini(TEXT_TO_EMBED)
    #     print(f"Embedding for '{TEXT_TO_EMBED}':")
    #     print(f"Vector length: {len(embedding)}")
    #     print(f"First 10 dimensions: {embedding[:10]}")
    # except ValueError as e:
    #     print(e)
    # except Exception as e:
    #     print(f"An error occurred: {e}")
