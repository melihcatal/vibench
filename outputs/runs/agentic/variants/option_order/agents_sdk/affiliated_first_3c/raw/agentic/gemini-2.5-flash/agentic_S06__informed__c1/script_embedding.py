import os
import google.generativeai as genai

def embed_script(text: str, api_key: str, model_name: str = "models/embedding-001") -> list:
    """
    Embeds a narration script using Gemini Embeddings via the Google Generative AI SDK.
    """
    genai.configure(api_key=api_key)

    try:
        response = genai.embed_content(
            model=model_name,
            content=text,
            task_type="RETRIEVAL_DOCUMENT" # Suitable for document search/retrieval
        )
        return response["embedding"]
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []
