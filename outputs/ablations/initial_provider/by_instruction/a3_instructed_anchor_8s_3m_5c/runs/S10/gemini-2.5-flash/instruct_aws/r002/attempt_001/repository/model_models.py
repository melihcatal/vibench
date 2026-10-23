import json
from typing import Dict, Any

def create_bedrock_request(prompt: str, max_tokens: int = 200, temperature: float = 0.5, top_p: float = 0.9) -> Dict[str, Any]:
    """
    Creates a standardized request body for Anthropic Claude models on AWS Bedrock.
    """
    return {
        "prompt": prompt,
        "max_tokens_to_sample": max_tokens,
        "temperature": temperature,
        "top_p": top_p
    }

def parse_bedrock_response(response_body: bytes) -> str:
    """
    Parses the response body from an AWS Bedrock invocation.
    """
    response_json = json.loads(response_body.decode("utf-8"))
    return response_json.get("completion", "")

def normalize_text_output(text: str) -> str:
    """
    Normalizes text output by stripping whitespace.
    """
    return text.strip()

