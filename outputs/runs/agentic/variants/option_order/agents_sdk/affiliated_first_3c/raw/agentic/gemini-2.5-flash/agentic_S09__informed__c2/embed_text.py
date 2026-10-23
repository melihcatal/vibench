import os
import google.generativeai as genai

def embed_text(text: str) -> list[float]:
    """Generates an embedding vector for a single text string using Google Gemini Embeddings."""
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    
    # Use the embedding model for text
    model = "models/embedding-001"
    
    response = genai.embed_content(
        model=model,
        content=text,
        task_type="RETRIEVAL_DOCUMENT" # or "SEMANTIC_SIMILARITY", "AQA", "CLASSIFICATION"
    )
    return response["embedding"]

if __name__ == '__main__':
    # Example usage (ensure GOOGLE_API_KEY is set in environment variables)
    # from dotenv import load_dotenv
    # load_dotenv()
    
    # text_to_embed = "The quick brown fox jumps over the lazy dog."
    # embedding = embed_text(text_to_embed)
    # print(f"Embedding for '{text_to_embed}': {embedding[:5]}...") # Print first 5 dimensions
    # print(f"Embedding length: {len(embedding)}")
    pass
