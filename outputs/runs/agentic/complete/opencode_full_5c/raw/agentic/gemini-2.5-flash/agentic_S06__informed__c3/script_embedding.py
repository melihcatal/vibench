from speech_client import get_embedding_model
from speech_models import EmbeddingRequest


def embed_script(request: EmbeddingRequest):
    model = get_embedding_model()
    response = model.embed_content(
        model_name="models/embedding-001", content=request.text
    )
    return response["embedding"]
