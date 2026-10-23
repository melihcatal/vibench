import json

def create_titan_embedding_request_body(text: str) -> str:
    return json.dumps({"inputText": text})

def parse_titan_embedding_response(response_body: str) -> list[float]:
    response_json = json.loads(response_body)
    return response_json.get("embedding", [])
