import google.generativeai as genai
from speech_client import configure_gemini_embeddings
from speech_models import EmbeddingRequest
from typing import List


def embed_script(request: EmbeddingRequest) -> List[float]:
    """Embeds narration scripts for voice-asset search using Gemini Embeddings."""
    configure_gemini_embeddings()

    if not genai.get_default_model():
        # Initialize a default model for embeddings if not already done
        # The specific model name for embeddings can vary; 'embedding-001' is a common one.
        # The user might need to ensure they have access to an embedding model.
        # For this example, we'll assume a default is configured or available.
        pass

    # The specific model name for embeddings might need to be passed as a parameter to embed_content
    # For this example, we'll use a commonly available embedding model if not specified.
    try:
        # As of recent updates, embedding can be directly called with a model name.
        # For general utility, we might want to allow passing the model name.
        # For now, let's use a common embedding model name.
        model_name = "models/embedding-001"
        response = genai.embed_content(
            model=model_name, content=request.text, task_type="RETRIEVAL_DOCUMENT"
        )
        return response["embedding"]
    except Exception as e:
        print(f"Error embedding content: {e}")
        return []
