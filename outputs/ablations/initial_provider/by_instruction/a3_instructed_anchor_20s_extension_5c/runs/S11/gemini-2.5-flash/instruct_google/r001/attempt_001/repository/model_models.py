from typing import Dict, Any

class ModelRequest:
    """
    A helper class to standardize model requests.
    """
    def __init__(self, prompt: str, **kwargs):
        self.prompt = prompt
        self.params = kwargs

    def to_dict(self) -> Dict[str, Any]:
        return {"prompt": self.prompt, **self.params}

class ModelResponse:
    """
    A helper class to standardize model responses.
    """
    def __init__(self, text: str, raw_response: Any = None, **kwargs):
        self.text = text
        self.raw_response = raw_response
        self.metadata = kwargs

    def to_dict(self) -> Dict[str, Any]:
        return {"text": self.text, "metadata": self.metadata}

def normalize_vertex_ai_response(response_object: Any) -> ModelResponse:
    """
    Normalizes a Google Cloud Vertex AI TextGenerationResponse to a ModelResponse.
    """
    if hasattr(response_object, 'text'):
        return ModelResponse(text=response_object.text, raw_response=response_object)
    return ModelResponse(text="", raw_response=response_object)
