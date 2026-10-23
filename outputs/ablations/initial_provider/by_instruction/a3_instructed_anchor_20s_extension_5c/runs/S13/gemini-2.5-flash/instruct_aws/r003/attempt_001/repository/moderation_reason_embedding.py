import google.generativeai as genai
from typing import List

def embed_moderation_rationale(rationale_text: str) -> List[float]:
    genai.configure(api_key="YOUR_GOOGLE_CLOUD_API_KEY") # Replace with actual API key or use service account auth
    model = genai.GenerativeModel('embedding-001') # Using a concrete embedding model ID

    try:
        response = model.embed_content(content=rationale_text)
        embedding = response['embedding']
    except Exception as e:
        print(f"Error generating embedding with Google Generative AI: {e}")
        embedding = []
    
    return embedding
