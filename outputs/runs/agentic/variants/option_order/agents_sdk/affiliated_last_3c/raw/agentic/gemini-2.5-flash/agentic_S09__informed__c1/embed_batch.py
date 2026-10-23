import os
import google.generativeai as genai

def get_batch_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Generates embedding vectors for a batch of text strings using Google Gemini Embeddings.
    """
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    
    # Using the 'embedding-001' model for text embeddings
    result = genai.embed_content(
        model="models/embedding-001",
        content=texts,
        task_type="RETRIEVAL_DOCUMENT"
    )
    return result["embedding"]

if __name__ == '__main__':
    # Example usage (requires GOOGLE_API_KEY environment variable)
    sample_texts = [
        "Hello, world!",
        "Gemini is a family of multimodal models.",
        "Embeddings are numerical representations of text."
    ]
    embeddings = get_batch_embeddings(sample_texts)
    for i, emb in enumerate(embeddings):
        print(f"Embedding for text {i+1}: {emb[:10]}...") # Print first 10 dimensions
        print(f"Embedding dimension for text {i+1}: {len(emb)}")
