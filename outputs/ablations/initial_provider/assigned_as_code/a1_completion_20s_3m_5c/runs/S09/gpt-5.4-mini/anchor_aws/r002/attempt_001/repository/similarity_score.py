from embeddings_client import get_client, get_config, invoke_embedding
from embeddings_models import cosine_similarity, normalize_embedding_response


def similarity_score(payload, config=None):
    config = get_config(config)
    client = get_client(config)
    left = normalize_embedding_response(invoke_embedding(client, config["model_id"], {"inputText": payload["text_a"]}))
    right = normalize_embedding_response(invoke_embedding(client, config["model_id"], {"inputText": payload["text_b"]}))
    return {"similarity": cosine_similarity(left, right)}
