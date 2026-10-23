import os
import google.generativeai as genai
from typing import List

def get_text_embedding_with_gemini(text_content: str) -> List[float]:
    """
    Embeds extracted document sections for semantic retrieval using Gemini Embeddings.
    """
    # Ensure GOOGLE_API_KEY is set in environment variables
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = "models/embedding-001"

    result = genai.embed_content(model=model, content=text_content)
    return result["embedding"]

if __name__ == '__main__':
    # Placeholder for actual usage, demonstrating the provider integration
    text_to_embed = "The quick brown fox jumps over the lazy dog."
    google_api_key = os.environ.get("GOOGLE_API_KEY")

    if google_api_key:
        print(f"Getting embedding for '{text_to_embed}' using Gemini Embeddings...")
        # embedding = get_text_embedding_with_gemini(text_to_embed)
        # print("Embedding (first 5 dimensions):", embedding[:5])
        # print("Embedding length:", len(embedding))
    else:
        print("Please set GOOGLE_API_KEY environment variable.")
