import json


def normalize_embedding_response(response):
    return json.loads(response["body"].read())["embedding"]
