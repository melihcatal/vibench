from typing import Dict, Any

class PlatformRequest:
    def __init__(self, prompt: str, **kwargs):
        self.prompt = prompt
        self.params = kwargs

    def to_vertex_ai_instance(self):
        return {"prompt": self.prompt, **self.params}

class PlatformResponse:
    def __init__(self, predictions: list, metadata: Dict[str, Any]):
        self.predictions = predictions
        self.metadata = metadata

    @classmethod
    def from_vertex_ai_response(cls, response: Any, model_id: str, project_id: str, location: str):
        metadata = {
            "model_id": model_id,
            "project_id": project_id,
            "location": location,
            "usage_tokens": len(str(response.predictions[0]).split()) # simplified token count
        }
        return cls(predictions=response.predictions, metadata=metadata)
