import os
import cohere
from speech_client import get_cohere_client
from speech_models import EmbeddingRequest, EmbeddingResult

def embed_script(request: EmbeddingRequest) -> EmbeddingResult:
    co = get_cohere_client()

    try:
        model_name = os.getenv("COHERE_EMBED_MODEL", "embed-english-v3.0")

        response = co.embed(
            texts=[request.text],
            model=model_name,
            input_type="search_document"
        )
        
        if response.embeddings and len(response.embeddings) > 0:
            return EmbeddingResult(embedding=response.embeddings[0])
        else:
            raise RuntimeError("Cohere API returned no embeddings.")

    except cohere.CohereAPIError as e:
        raise RuntimeError(f"Cohere API request failed: {e}")
    except Exception as e:
        raise RuntimeError(f"An unexpected error occurred during Cohere embedding: {e}")
