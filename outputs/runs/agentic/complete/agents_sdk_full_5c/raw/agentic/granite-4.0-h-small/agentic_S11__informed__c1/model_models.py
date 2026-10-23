from typing import Dict, Any, Optional

class GenerationRequest:
    """Container for model invocation parameters."""
    def __init__(self, deployment: str, prompt: str, temperature: float = 0.7,
                 max_tokens: int = 256, stream: bool = False):
        self.deployment = deployment
        self.prompt = prompt
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.stream = stream

class GenerationResponse:
    """Parsed response from a managed model invocation."""
    def __init__(self, text: str, usage: Dict[str, int], deployment_id: str,
                 raw: Any):
        self.text = text
        self.usage = usage
        self.deployment_id = deployment_id
        self.raw = raw  # Raw provider response object
