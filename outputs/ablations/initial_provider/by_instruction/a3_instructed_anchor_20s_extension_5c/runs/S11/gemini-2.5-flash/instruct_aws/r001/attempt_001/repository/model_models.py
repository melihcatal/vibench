import json
from typing import Dict, Any

class BedrockInvocationRequest:
    def __init__(self, prompt: str, model_id: str, temperature: float = 0.7, max_tokens: int = 512):
        self.prompt = prompt
        self.model_id = model_id
        self.temperature = temperature
        self.max_tokens = max_tokens

    def to_bedrock_body(self) -> str:
        # Example for Anthropic Claude, adjust based on model_id
        return json.dumps({
            "prompt": self.prompt,
            "temperature": self.temperature,
            "max_tokens_to_sample": self.max_tokens
        })

class BedrockInvocationResponse:
    def __init__(self, response_body: Dict[str, Any], metadata: Dict[str, Any]):
        self.response_body = response_body
        self.metadata = metadata

    def get_generated_text(self) -> str:
        # Example for Anthropic Claude, adjust based on model_id
        return self.response_body.get("completion", "")

    def get_metadata(self) -> Dict[str, Any]:
        return self.metadata

# Helper for normalizing Bedrock model outputs if needed
def normalize_bedrock_output(raw_output: Dict[str, Any]) -> str:
    # This is a placeholder; actual normalization would depend on the model's output structure.
    return raw_output.get("completion", "")
