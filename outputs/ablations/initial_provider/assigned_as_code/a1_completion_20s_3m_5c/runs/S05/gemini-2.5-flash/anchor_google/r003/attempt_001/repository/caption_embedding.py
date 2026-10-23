import os
import google.generativeai as genai
from speech_models import EmbeddingResult

def embed_caption_chunk(text_chunk: str) -> EmbeddingResult:
    """Generates embeddings for a caption chunk using Google's Generative AI Embedding model."""
    # Ensure GOOGLE_API_KEY environment variable is set for Generative AI
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=google_api_key)

    # Use the specific embedding model, e.g., 'embedding-001'
    model = genai.GenerativeModel('embedding-001')

    try:
        response = model.embed_content(content=text_chunk, task_type="SEMANTIC_SIMILARITY")
        embedding = response['embedding']
        return EmbeddingResult(embedding=embedding)
    except Exception as e:
        print(f"Error generating embedding with Generative AI: {e}")
        return EmbeddingResult(embedding=[]) # Return empty embedding on error
