
import json
from typing import Any, Dict, List, Optional

class ManagedModelRequest:
    """
    Represents a standardized request structure for invoking a managed model.
    This can be transformed into a provider-specific request format.
    """
    def __init__(self, prompt: str, parameters: Optional[Dict[str, Any]] = None):
        self.prompt = prompt
        self.parameters = parameters if parameters is not None else {}

    def to_provider_format(self, provider: str = "vertex_ai") -> Dict[str, Any]:
        """
        Converts the standardized request to a provider-specific format.
        For Google Cloud Vertex AI, this might involve structuring for `predict` method.
        """
        if provider == "vertex_ai":
            # Example for Vertex AI's text-bison model or similar
            instances = [{"prompt": self.prompt}]
            return {
                "instances": instances,
                "parameters": self.parameters
            }
        # Add other providers here
        raise ValueError(f"Unknown provider: {provider}")

class ManagedModelResponse:
    """
    Represents a standardized response structure from a managed model.
    This can encapsulate various provider-specific response formats.
    """
    def __init__(self, raw_response: Dict[str, Any], provider: str = "vertex_ai"):
        self.raw_response = raw_response
        self.provider = provider
        self.text_output: Optional[str] = None
        self._parse_response()

    def _parse_response(self):
        """
        Parses the raw provider response into a standardized format.
        """
        if self.provider == "vertex_ai":
            # Example for Vertex AI's text-bison model or similar
            predictions = self.raw_response.get("predictions", [])
            if predictions:
                # Assuming the first prediction contains the text output
                self.text_output = predictions[0].get("content")
        # Add other providers here
        else:
            self.text_output = json.dumps(self.raw_response) # Default to raw JSON string for unknown providers

    def get_text_output(self) -> Optional[str]:
        """
        Returns the normalized text output from the model.
        """
        return self.text_output

def normalize_model_output(raw_output: Dict[str, Any], provider: str = "vertex_ai") -> ManagedModelResponse:
    """
    Normalizes a raw model output (from any provider) into a standardized
    ManagedModelResponse object.
    """
    return ManagedModelResponse(raw_output, provider)
