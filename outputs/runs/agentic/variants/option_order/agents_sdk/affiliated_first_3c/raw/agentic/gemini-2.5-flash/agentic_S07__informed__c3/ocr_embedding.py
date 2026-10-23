import os
import google.generativeai as genai
from document_models import EmbeddingResponse

def get_text_embedding(text: str) -> EmbeddingResponse:
    """
    Embeds extracted document sections for semantic retrieval using Gemini Embeddings.
    """
    # Configure with your Google API Key
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    model = "models/embedding-001"
    
    try:
        response = genai.embed_content(
            model=model,
            content=text,
            task_type="RETRIEVAL_DOCUMENT" # or "RETRIEVAL_QUERY", "SEMANTIC_SIMILARITY", etc.
        )
        embedding = response['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        embedding = [] # Return empty list on error
            
    return EmbeddingResponse(embedding=embedding)

