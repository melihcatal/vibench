import os
import google.generativeai as genai

def embed_moderation_rationales(rationales: list[str]) -> list[list[float]]:
    """
    Embeds moderation rationales for case retrieval using Google's Generative AI.

    Args:
        rationales: A list of strings, where each string is a moderation rationale.

    Returns:
        A list of embeddings, where each embedding is a list of floats.
    """
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('embedding-001')
    
    embeddings = []
    for rationale in rationales:
        response = model.embed_content(model='embedding-001', content=rationale)
        embeddings.append(response['embedding'])
    
    return embeddings
