import google.generativeai as genai
import os
from typing import List, Dict, Any

def embed_ocr_text(text_sections: List[str], model_name: str = "models/embedding-001") -> List[List[float]]:
    """Embeds extracted document sections using Gemini Embeddings for semantic retrieval."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    # The embedding model to use
    # model_name = "models/embedding-001"

    if not text_sections:
        return []

    embeddings = []
    for text in text_sections:
        response = genai.embed_content(model=model_name, content=text)
        embeddings.append(response["embedding"])
    
    return embeddings

if __name__ == '__main__':
    # Placeholder for actual usage. Ensure GOOGLE_API_KEY is set.
    sample_sections = [
        "The quick brown fox jumps over the lazy dog.",
        "Artificial intelligence is rapidly advancing.",
        "Gemini is a family of multimodal models developed by Google AI."
    ]

    try:
        # text_embeddings = embed_ocr_text(sample_sections)
        # for i, embedding in enumerate(text_embeddings):
        #     print(f"Embedding for section {i+1} (first 5 elements): {embedding[:5]}...")
        print("Run with an actual Google API Key and enable the Gemini API in your project.")
    except Exception as e:
        print(f"Error generating embeddings: {e}")
