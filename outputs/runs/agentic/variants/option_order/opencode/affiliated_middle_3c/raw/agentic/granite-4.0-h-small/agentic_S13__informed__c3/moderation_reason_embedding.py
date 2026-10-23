from ibm_watsonx_ai.nlp import EmbeddingModel
import os

# watsonx.ai embeddings integration (later-step)
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
model = EmbeddingModel(service_instance_id=WATSONX_PROJECT_ID, api_key=WATSONX_API_KEY)


def embed_moderation_rationale(text: str) -> list[float]:
    """Embeds a moderation rationale for similarity retrieval.

    Args:
        text (str): Rationale/explanation provided by moderation service.

    Returns:
        list[float]: Embedding vector representing the rationale.
    """
    return model.get_text_embedding(text)["embedding"]
