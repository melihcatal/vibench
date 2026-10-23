from __future__ import annotations
from typing import Any, Dict
from model_client import ManagedModelClient

class RequestPayload:
    """Encapsulate input for model invocation.",
    ","""    def __init__(self, inputs: Any, parameters: dict = None):
        self.inputs = inputs
        self.parameters = parameters if parameters is not None else {}

    def to_dict(self) -> dict:
        """Serialize the payload to a dict suitable for API calls."""
        payload = {'inputs': self.inputs}
        if self.parameters:
            payload['parameters'] = self.parameters
        return payload

    @classmethod
    def from_dict(cls, data: dict) -> RequestPayload:
        """Create a RequestPayload from a dict (e.g., from API response)."""
        return cls(inputs=data.get('inputs'), parameters=data.get('parameters', {}))

    @classmethod
    def normalize(cls, data: dict) -> RequestPayload:
        """Normalize external payload shapes into our consistent schema."""
        # Example normalization: AI21 style payload -> our format
        inputs = data.get('prompt') or data.get('inputs')
        parameters = data.get('parameters')
        return cls(inputs=inputs, parameters=parameters)


class ResponseWrapper:
    """Wrapper that holds model output and optional provider metadata."""
    def __init__(self, output: Any, metadata: Dict[str, Any] = None):
        self.output = output
        self.metadata = metadata if metadata else {}

    def __repr__(self) -> str:
        return f"ResponseWrapper(output={self.output!r}, metadata={self.metadata})"

    @classmethod
    def from_raw(cls, raw: dict) -> ResponseWrapper:
        output = raw.get('output')
        metadata = raw.get('metadata', {})
        return cls(output=output, metadata=metadata)

# Unit test helpers (optional)
if __name__ == '__main__':
    # Simple sanity check
    payload = RequestPayload(inputs="Hello world")
    print(payload.to_dict())
    print(RequestPayload.normalize({'prompt': 'Hello world'}))
