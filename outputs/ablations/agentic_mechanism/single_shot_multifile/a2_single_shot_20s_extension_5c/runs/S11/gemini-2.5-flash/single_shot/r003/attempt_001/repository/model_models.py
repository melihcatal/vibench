import json

def get_claude_request_body(prompt: str, max_tokens: int = 100) -> str:
    return json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    })

def parse_claude_response(response_body: str) -> str:
    response_json = json.loads(response_body)
    return response_json["content"][0]["text"]

def parse_claude_stream_chunk(chunk: dict) -> str:
    if "chunk" in chunk:
        chunk_data = json.loads(chunk["chunk"]["bytes"].decode("utf-8"))
        if chunk_data["type"] == "content_block_delta" and chunk_data["delta"]["type"] == "text_delta":
            return chunk_data["delta"]["text"]
    return ""

def parse_titan_embedding_response(response_body: str) -> list[float]:
    response_json = json.loads(response_body)
    return response_json["embedding"]
