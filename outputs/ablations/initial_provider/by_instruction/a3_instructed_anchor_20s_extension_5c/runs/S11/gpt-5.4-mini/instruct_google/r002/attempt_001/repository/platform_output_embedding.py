from model_client import get_default_model, get_google_client
from model_models import PlatformRequest


def platform_output_embedding(request: PlatformRequest):
    client = get_google_client()
    model_name = request.model or get_default_model()
    response = client.models.embed_content(model=model_name, contents=request.prompt)
    return {"model": model_name, "embedding": getattr(response, "embedding", None) or response.embeddings}
