import os
import google.generativeai as genai
from speech_models import EmbeddingPayload

def transcript_embedding(payload: EmbeddingPayload):
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    if not os.environ.get("GEMINI_API_KEY"):
        raise ValueError("Gemini API key not found. Please set GEMINI_API_KEY environment variable.")

    model = genai.GenerativeModel('text-embedding-004') # Using a specific embedding model
    
    embeddings = []
    for segment in payload.text_segments:
        response = model.embed_content(content=segment)
        embeddings.append(response['embedding'])
    
    return {"embeddings": embeddings}
