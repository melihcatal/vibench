import os
import google.generativeai as genai
from typing import List

def embed_transcript_segments(text_segments: List[str], model_name: str = "models/embedding-001") -> List[List[float]]:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Google API Key not provided and GOOGLE_API_KEY environment variable not set.")
    
    genai.configure(api_key=api_key)

    embeddings = []
    for text in text_segments:
        result = genai.embed_content(model=model_name, content=text)
        embeddings.append(result['embedding'])
    return embeddings
