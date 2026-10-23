from embeddings_client import get_bedrock_client, get_model_id, invoke_bedrock_json
from embeddings_models import cosine_similarity, parse_embedding_response


def similarity_score(payload, config=None):
    config = config or {}
    client = get_bedrock_client(config)
    model_id = get_model_id(config)
    left = invoke_bedrock_json(client, model_id, {"inputText": payload["text1"]})
    right = invoke_bedrock_json(client, model_id, {"inputText": payload["text2"]})
    left_embedding = parse_embedding_response(left)
    right_embedding = parse_embedding_response(right)
    return {"score": cosine_similarity(left_embedding, right_embedding)}
