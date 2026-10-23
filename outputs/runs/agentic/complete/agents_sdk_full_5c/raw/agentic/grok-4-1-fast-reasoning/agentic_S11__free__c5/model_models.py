import json
from typing import Dict, Any, Optional

def build_bedrock_anthropic_request(
    prompt: str,
    max_tokens: int = 1024,
    temperature: float = 0.7
) -> Dict[str, Any]:
    return {
        'anthropic_version': 'bedrock-2023-05-31',
        'max_tokens': max_tokens,
        'temperature': temperature,
        'messages': [{'role': 'user', 'content': prompt}]
    }

def parse_bedrock_invoke_response(body_bytes: bytes) -> Dict[str, Any]:
    return json.loads(body_bytes.decode('utf-8'))