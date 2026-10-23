from typing import Dict, Any


class ModelRequest:
    def __init__(self, prompt: str, parameters: Dict[str, Any] = None):
        self.prompt = prompt
        self.parameters = parameters if parameters is not None else {}


class ModelResponse:
    def __init__(self, generated_text: str, metadata: Dict[str, Any] = None):
        self.generated_text = generated_text
        self.metadata = metadata if metadata is not None else {}

    @classmethod
    def from_huggingface_response(cls, hf_response: Any, model_id: str = None):
        generated_text = (
            hf_response.generated_text
            if hasattr(hf_response, "generated_text")
            else str(hf_response)
        )
        metadata = {}
        if hasattr(hf_response, "details") and hf_response.details:
            metadata["details"] = hf_response.details.to_dict()
        if model_id:
            metadata["model_id"] = model_id
        return cls(generated_text=generated_text, metadata=metadata)
