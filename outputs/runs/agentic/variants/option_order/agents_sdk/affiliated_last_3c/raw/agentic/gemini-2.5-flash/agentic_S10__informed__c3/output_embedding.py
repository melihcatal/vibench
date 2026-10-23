import openai
import os

def get_text_embedding(text: str, model: str = "text-embedding-ada-002") -> list:
    """
    Embeds model outputs for clustering or retrieval using OpenAI Embeddings.
    """
    openai.api_key = os.environ.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    response = openai.Embedding.create(
        input=text,
        model=model
    )
    return response['data'][0]['embedding']
