from typing import Any, Dict, Optional

class ModelDescriptor:
    """Simple container for a resolved model/deployment identifier."""
    def __init__(self, resource_type: str, identifier: str):
        self.resource_type = resource_type  # e.g., 'model', 'deployment', 'inference_profile'
        self.identifier = identifier  # provider-specific ID

class ModelRequest:
    """Normalized request payload for invoke calls across providers."""
    def __init__(
        self,
        deployment: str,
        prompt: str,
        temperature: float = 0.0,
        max_tokens: Optional[int] = None,
        **kwargs: Any,
    ):
        self.deployment = deployment  # provider model/deployment ID
        self.prompt = prompt  # user input text
        self.temperature = temperature  # provider temperature/control param
        self.max_tokens = max_tokens  # provider max output length param
        # Additional provider-specific parameters can be added via kwargs
        self.extra_params = kwargs

class ModelResponse:
    """Container for the model output plus platform metadata."""
    def __init__(self, output: str, metadata: Dict[str, Any]):
        self.output = output  # raw text returned by the provider
        self.metadata = metadata  # dict containing usage stats, resource IDs, timestamps, etc.
