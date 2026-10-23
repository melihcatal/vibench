import json

def create_titan_text_embedding_payload(text):
    return json.dumps({"inputText": text})

def parse_titan_text_embedding_response(response_body):
    return json.loads(response_body.read())["embedding"]

def create_titan_multimodal_embedding_payload(text_segment):
    return json.dumps({"text": text_segment})

def parse_titan_multimodal_embedding_response(response_body):
    return json.loads(response_body.read())
