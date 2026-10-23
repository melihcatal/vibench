import os
import google.generativeai as genai

def get_caption_embedding(caption_text: str, model_name: str = "embedding-001") -> list[float]:
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable must be set for Google Generative AI.")

    genai.configure(api_key=api_key)

    result = genai.embed_content(
        model=model_name,
        content=caption_text,
        task_type="RETRIEVAL_DOCUMENT"
    )

    return result['embedding']
