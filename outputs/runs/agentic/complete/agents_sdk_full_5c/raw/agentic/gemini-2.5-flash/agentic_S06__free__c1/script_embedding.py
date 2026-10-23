import os
import google.generativeai as genai

def embed_narration_script(text: str, api_key: str, model_name: str = "embedding-gecko-001") -> list:
    """Embeds narration scripts for voice-asset search using Google Generative AI (PaLM API).

    Args:
        text: The narration script content to embed.
        api_key: Your Google Generative AI API key.
        model_name: The name of the embedding model to use (e.g., "embedding-gecko-001").

    Returns:
        A list of floats representing the embedding vector.
    """
    genai.configure(api_key=api_key)

    try:
        response = genai.embed_content(
            model=model_name,
            content=text,
        )
        return response['embedding']
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return []
