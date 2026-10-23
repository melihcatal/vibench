from model_client import get_text_embedding_model
from model_models import ModelResponse


def embed_platform_outputs(texts: list[str]) -> ModelResponse:
    model = get_text_embedding_model()
    embeddings = model.get_embeddings(texts)
    # The raw_response here will be the list of embedding objects from the model
    return ModelResponse(
        text="",
        raw_response=[e.values for e in embeddings],
        metadata={"embedding_model": model.model_id},
    )
