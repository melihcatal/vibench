import json
from typing import Dict, Any, List

def build_claude_body(
    prompt: str,
    max_tokens: int = 1024,
    temperature: float = 0.7
) -> str:
    messages = [{"role": "user", "content": prompt}]
    return json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": messages
    })

def parse_claude_completion(response: Dict[str, Any]) -> str:
    return response['content'][0]['text']

def parse_claude_usage(response: Dict[str, Any]) -> Dict[str, int]:
    usage = response.get('usage', {})
    return {
        'input_tokens': usage.get('inputTokens', 0),
        'output_tokens': usage.get('outputTokens', 0)
    }
