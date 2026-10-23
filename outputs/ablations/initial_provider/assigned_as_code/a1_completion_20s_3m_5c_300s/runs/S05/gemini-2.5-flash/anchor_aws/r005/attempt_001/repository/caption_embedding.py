import google.generativeai as genai
import os

def initialize_embedding_model():
    """Initializes the Google Generative AI embedding model client."""
    # Ensure GOOGLE_API_KEY environment variable is set
    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    # Use a specific embedding model
    return genai.GenerativeModel('embedding-001') # Provider-specific model ID

def get_caption_embedding(text_chunk: str) -> list[float]:
    """Generates an embedding for a given caption chunk using Google Generative AI."""
    model = initialize_embedding_model()

    # The embedding API expects a list of strings, even for a single string
    response = model.embed_content(content=[text_chunk], task_type="SEMANTIC_SIMILARITY")
    
    # The response contains embedding values in a structure. Extract the embedding vector.
    if response.embeddings and response.embeddings[0].values:
        return response.embeddings[0].values
    return []
