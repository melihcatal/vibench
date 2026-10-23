from embeddings_client import load_config, invoke_embeddings
from embeddings_models import BatchEmbeddingRequest, extract_embeddings, normalize_vector


def embed_batch(texts):
    cfg = load_config()
    request = BatchEmbeddingRequest(texts=list(texts))
    payload = {"inputTextList": request.texts}
    response = invoke_embeddings(cfg.model_id, payload, cfg.region_name)
    return [normalize_vector(vector) for vector in extract_embeddings(response)]
