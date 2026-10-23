from typing import Any, Dict, List

class ModelDescriptor:
    """
    Simple immutable holder for a resolved model reference.
    Contains the provider name and the service‑specific model identifier.
    """
    def __init__(self, service: str, model: str):
        self.service = service
        self.model = model

    def __repr__(self) -> str:
        return f"ModelDescriptor(service={self.service!r}, model={self.model!r})"


class ModelInvocationRequest:
    """
    Generic request payload that can be passed to ManagedModelClient.invoke.
    Provider‑specific fields (model, parameters, messages, stream flag) are stored as a dict
    to remain agnostic of the underlying SDK.
    """
    def __init__(self, model: str, parameters: Dict[str, Any], messages: List[Dict[str, str]], stream: bool = False):
        # Provider‑agnostic representation; concrete client will translate as needed.
        self._payload = {
            'model': model,
            'parameters': parameters,
            'messages': messages,
            'stream': stream,
        }

    @property
    def raw(self) -> Dict[str, Any]:
        return self._payload

    def __repr__(self) -> str:
        return f"ModelInvocationRequest({self._payload!r})"


class InvocationResponse:
    """
    Wrapper for the raw provider response.
    Provides easy access to generated text and any metadata fields (request_id, usage, etc.).
    """
    def __init__(self, raw: Any):
        self.raw = raw

    @property
    def generated_text(self) -> str:
        """Extract the model output. Adjust extraction logic per provider."""
        # Example for Vertex AI streaming response
        if hasattr(self.raw, 'candidates'):
            # Vertex AI generates a list of candidates
            return self.raw.candidates[0].content.parts[0].text
        # Example for Azure OpenAI completion
        if hasattr(self.raw, 'choices'):
            return self.raw.choices[0].message.content
        # Default fallback: assume a simple dict with a 'text' key
        return str(self.raw.get('text', ''))

    @property
    def request_id(self) -> Optional[str]:
        return self.raw.get('requestId') or self.raw.get('id')

    @property
    def usage(self) -> Optional[Dict[str, Any]]:
        return self.raw.get('usage')

    def __repr__(self) -> str:
        return f"InvocationResponse(generated_text={self.generated_text!r})"
