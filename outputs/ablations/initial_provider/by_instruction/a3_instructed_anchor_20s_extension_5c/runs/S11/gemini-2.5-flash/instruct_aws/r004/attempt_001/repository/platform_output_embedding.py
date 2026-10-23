import os
import google.generativeai as genai

def embed_platform_output(text: str, model_name: str = "models/embedding-001") -> dict:
    """
    Embeds platform outputs for evaluation or retrieval using Google AI Embeddings.

    Args:
        text (str): The text content to embed.
        model_name (str): The name of the embedding model to use (e.g., "models/embedding-001").

    Returns:
        dict: The embedding result from Google AI.
    """
    # Ensure GOOGLE_API_KEY is set in environment variables for generativeai
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    response = genai.embed_content(model=model_name, content=text)
    
    embedding = response['embedding']
    return {"embedding": embedding, "raw_response": response}
