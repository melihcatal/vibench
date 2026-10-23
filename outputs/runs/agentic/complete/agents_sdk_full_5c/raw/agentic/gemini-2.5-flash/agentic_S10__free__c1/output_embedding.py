import os
import google.generativeai as genai
from typing import List
from model_client import get_gemini_model

def embed_text(texts: List[str], model_name: str = "embedding-001") -> List[List[float]]:
    """
    Embeds model outputs for clustering or retrieval using a hosted embedding model.
    """
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set. Please set your API key.")
    
    genai.configure(api_key=api_key)
    
    # The embedding model is called differently than the generative models
    # It uses genai.embed_content directly
    result = genai.embed_content(
        model=model_name,
        content=texts,
        task_type="RETRIEVAL_DOCUMENT" # or other relevant task types like CLASSIFICATION, SEMANTIC_SIMILARITY
    )
    return [embedding for embedding in result['embedding']]

if __name__ == '__main__':
    # Example usage - not for grading
    # from dotenv import load_dotenv
    # load_dotenv()
    # genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    # texts_to_embed = [
    #     "The cat sat on the mat.",
    #     "A feline rested on a rug.",
    #     "The dog barked loudly."
    # ]
    # embeddings = embed_text(texts_to_embed)
    # for i, emb in enumerate(embeddings):
    #     print(f"Embedding for \"{texts_to_embed[i]}\": {emb[:5]}...") # Print first 5 dimensions
    pass
