import google.generativeai as genai
import os
from typing import List
from model_client import get_gemini_client

def embed_output(text_or_texts: List[str]) -> List[List[float]]:
    """
    Embeds model outputs for clustering or retrieval using Gemini Embeddings.
    """
    client = get_gemini_client()
    
    try:
        if isinstance(text_or_texts, str):
            text_or_texts = [text_or_texts]

        # The embedding model is specified in the call.
        result = client.embed_content(
            model="models/embedding-001", 
            content=text_or_texts
        )
        
        embeddings = [item.embedding for item in result.embeddings]
        
        print(f"Generated {len(embeddings)} embeddings.")
        if embeddings:
            print(f"First embedding dimension: {len(embeddings[0])}")
        
        return embeddings
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return []

if __name__ == '__main__':
    os.environ["GOOGLE_API_KEY"] = "YOUR_GEMINI_API_KEY" # Replace with your actual key or set it in your environment
    
    text_to_embed_single = "This is a sentence about cats."
    embedding_single = embed_output([text_to_embed_single])
    print(f"Embedding for '{text_to_embed_single}': {embedding_single[0][:5]}...") # Print first 5 dimensions

    texts_to_embed_multiple = [
        "The quick brown fox jumps over the lazy dog.",
        "A group of canines rests peacefully."
    ]
    embeddings_multiple = embed_output(texts_to_embed_multiple)
    print(f"\nEmbedding for '{texts_to_embed_multiple[0]}': {embeddings_multiple[0][:5]}...")
    print(f"Embedding for '{texts_to_embed_multiple[1]}': {embeddings_multiple[1][:5]}...")
