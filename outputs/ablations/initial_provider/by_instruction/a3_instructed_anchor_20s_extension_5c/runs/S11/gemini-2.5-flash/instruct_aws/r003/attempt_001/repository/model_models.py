import json
from typing import Dict, Any

class BedrockInvokeRequest:
    def __init__(self, prompt: str, max_tokens: int = 300, temperature: float = 0.5, **kwargs):
        self.prompt = prompt
        self.max_tokens_to_sample = max_tokens
        self.temperature = temperature
        self.additional_params = kwargs

    def to_json_string(self) -> str:
        body = {
            "prompt": f"\n\nHuman: {self.prompt}\n\nAssistant:",
            "max_tokens_to_sample": self.max_tokens_to_sample,
            "temperature": self.temperature,
        }
        body.update(self.additional_params)
        return json.dumps(body)

class BedrockInvokeResponse:
    def __init__(self, response_body: Dict[str, Any]):
        self.completion = response_body.get("completion", "")
        self.stop_reason = response_body.get("stop_reason", None)
        self.stop_sequence = response_body.get("stop_sequence", None)
        self.usage = response_body.get("usage", {})

    def get_completion(self) -> str:
        return self.completion

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "stop_reason": self.stop_reason,
            "stop_sequence": self.stop_sequence,
            "usage": self.usage
        }

def normalize_bedrock_response(raw_response_body: str) -> BedrockInvokeResponse:
    """Normalizes a raw Bedrock response body string into a structured object.

    Args:
        raw_response_body (str): The raw JSON string received from Bedrock.

    Returns:
        BedrockInvokeResponse: A structured response object.
    """
    parsed_body = json.loads(raw_response_body)
    return BedrockInvokeResponse(parsed_body)
