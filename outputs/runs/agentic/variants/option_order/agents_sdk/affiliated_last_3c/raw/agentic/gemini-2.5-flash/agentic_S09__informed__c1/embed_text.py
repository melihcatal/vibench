import os
import google.generativeai as genai

def get_text_embedding(text: str) -> list[float]:
    """
    Generates an embedding vector for a single text string using Google Gemini Embeddings.
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    
    # Using the 'embedding-001' model for text embeddings
    result = genai.embed_content(
        model="models/embedding-001",
        content=[text],
        task_type="RETRIEVAL_DOCUMENT"
    )
    return result["embedding"][0]

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY environment variable)
    sample_text = "The quick brown fox jumps over the lazy dog."
    embedding = get_text_embedding(sample_text)
    print(f"Embedding for text: {embedding[:10]}...") # Print first 10 dimensions
    print(f"Embedding dimension: {len(embedding)}")
