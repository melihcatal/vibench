import json

def prepare_bedrock_payload(text):
    return json.dumps({"inputText": text})

def parse_bedrock_response(response_body):
    stream = response_body
    try:
        return json.loads(stream.read())["embedding"]
    finally:
        stream.close()
