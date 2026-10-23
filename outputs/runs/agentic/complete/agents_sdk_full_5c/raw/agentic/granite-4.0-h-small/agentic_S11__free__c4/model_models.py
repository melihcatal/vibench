# model_models.py
# [HELPER] Managed Model Platform Workflow - request/response normalization and helpers

from typing import Dict, Any, List, Optional

# Minimal model-agnostic wrappers for request/response shapes

class ModelInvocationRequest:
    """Abstract representation of a request to invoke a model."
    
    def __init__(self, deployment: str, prompt: str, temperature: float = 0.7):
        self.deployment = deployment    # provider-specific deployment ID
        self.prompt = prompt            # raw user prompt
        self.temperature = temperature  # sampling control

    def to_dict(self) -> Dict[str, Any]:
        return {
            "deployment": self.deployment,
            "prompt": self.prompt,
            "temperature": self.temperature,
        }


class ModelInvocationResponse:
    """Abstract representation of a model invocation response from any provider."
    
    def __init__(self, raw: Dict[str, Any]):
        self.raw = raw  # raw provider payload (kept for later augmentation)

    @property
    def choices(self) -> List[Dict[str, Any]]:
        return self.raw.get("choices", [])

    @property
    def usage(self) -> Dict[str, Any]:
        return self.raw.get("usage", {})

    @property
    def model(self) -> Optional[str]:
        return self.raw.get("model")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "choices": self.choices,
            "usage": self.usage,
            "model": self.model,
        }


class ModelSpec:
    """Describes a model catalog entry (provider-specific)."
    
    def __init__(self, name: str, family: str, version: str, description: Optional[str] = None):
        self.name = name
        self.family = family
        self.version = version
        self.description = description

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "family": self.family,
            "version": self.version,
            "description": self.description,
        }


class DeploymentSpec:
    """Describes a deployment entry for a model."
    
    def __init__(self, name: str, model_name: str, max_latency: str = "0s"):
        self.name = name
        self.model_name = model_name
        self.max_latency = max_latency

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "model_name": self.model_name,
            "max_latency": self.max_latency,
        }
