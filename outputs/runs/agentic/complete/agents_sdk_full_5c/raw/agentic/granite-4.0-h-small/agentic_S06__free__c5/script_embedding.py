# script_embedding.py
# [LATER-STEP] Embed narration scripts for voice-asset search using Cohere Embeddings.

import os
import cohere
from speech_client import get_texttospeech_client  # reuse ADC handling

def embed_script(script: str, model: str = 'embed-english-light-v3.0') -> list[float]:
    """Generate an embedding vector for a narration script using Cohere.

    Args:
        script: Plain text or SSML script.
        model: Cohere model identifier for embeddings.

    Returns:
        List of floats representing the embedding.
    """
    # Cohere client reads credentials from environment variable COHERE_API_KEY
    client = cohere.Client()  
    response = client.embed(text=script, model=model)
    # response.embeddings is a list of floats
    return response.embeddings
