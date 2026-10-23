import google.generativeai as genai
import os

def embed_translated_segment(segment_text: str) -> list[float]:
    """
    Embeds a translated text segment for translation-memory search using Gemini Embeddings.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = 'models/embedding-001'

    response = genai.embed_content(
        model=model,
        content=segment_text,
        task_type="RETRIEVAL_DOCUMENT" # or "RETRIEVAL_QUERY" depending on use case
    )
    return response['embedding']
