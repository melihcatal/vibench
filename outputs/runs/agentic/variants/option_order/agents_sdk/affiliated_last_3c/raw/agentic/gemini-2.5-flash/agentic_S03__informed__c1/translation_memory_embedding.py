import google.generativeai as genai
import os
from typing import List
from translation_models import EmbeddingRequest, EmbeddingResponse

def embed_translation_segments(request: EmbeddingRequest) -> EmbeddingResponse:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    
    # Using a specific embedding model from Gemini API
    # The `embed_content` function directly calls the embedding model.
    embeddings = []
    for text in request.text_segments:
        result = genai.embed_content(
            model="models/embedding-001",
            content=text,
            task_type="RETRIEVAL_DOCUMENT" # or other suitable task_type
        )
        embeddings.append(result['embedding'])
    
    return EmbeddingResponse(embeddings=embeddings)
