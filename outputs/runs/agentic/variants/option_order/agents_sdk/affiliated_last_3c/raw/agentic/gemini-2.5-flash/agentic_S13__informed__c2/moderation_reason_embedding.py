import os
import google.generativeai as genai

def moderation_reason_embedding(reason_text: str) -> list:
    """
    Embeds moderation rationales for case retrieval using Google Gemini Embeddings.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    model = 'models/embedding-001'

    # The embedding API expects a list of texts, even if it's a single one.
    response = genai.embed_content(model=model, content=[reason_text])
    
    # The response contains a list of embeddings. For a single text, we take the first one.
    return response['embedding'][0]
