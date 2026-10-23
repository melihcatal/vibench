from embeddings_client import load_config, invoke_embeddings
from embeddings_models import TextEmbeddingRequest, extract_embedding, normalize_vector


def embed_text(text: str):
    cfg = load_config()
    request = TextEmbeddingRequest(text=text)
    payload = {"inputText": request.text}
    response = invoke_embeddings(cfg.model_id, payload, cfg.region_name)
    return normalize_vector(extract_embedding(response))
