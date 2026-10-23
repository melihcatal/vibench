from embeddings_client import get_bedrock_client, get_model_id, invoke_embedding
from embeddings_models import normalize_texts, parse_embedding_response


def embed_batch(payload, config=None):
    texts = normalize_texts(payload)
    client = get_bedrock_client(config)
    model_id = get_model_id(config)
    embeddings = []
    for text in texts:
        response = invoke_embedding(client, model_id, text)
        embeddings.append(parse_embedding_response(response)["embedding"])
    return {"embeddings": embeddings}
