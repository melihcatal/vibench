import os
import google.generativeai as genai
from typing import List

def embed_ocr_text_sections(texts: List[str]) -> List[List[float]]:
    """
    Embeds extracted document sections for semantic retrieval using Google Gemini Embeddings.
    Requires GOOGLE_API_KEY to be set.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Google API Key not found. Set GOOGLE_API_KEY environment variable.")
    
    genai.configure(api_key=api_key)

    model = "embedding-001"
    
    # The Gemini API supports batching for embeddings
    embeddings = []
    response = genai.embed_content(
        model=model,
        content=texts
    )
    
    for embedding_data in response['embedding']:
        embeddings.append(embedding_data)

    return embeddings

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY set)
    # document_sections = [
    #     "This is the first paragraph of the document.",
    #     "The quick brown fox jumps over the lazy dog.",
    #     "Financial data for Q3 shows significant growth in revenue."
    # ]
    #
    # embedded_vectors = embed_ocr_text_sections(document_sections)
    # for i, vector in enumerate(embedded_vectors):
    #     print(f"Embedding for section {i+1} (first 5 dims): {vector[:5]}...")
    #     print(f"Vector length: {len(vector)}")
    pass
