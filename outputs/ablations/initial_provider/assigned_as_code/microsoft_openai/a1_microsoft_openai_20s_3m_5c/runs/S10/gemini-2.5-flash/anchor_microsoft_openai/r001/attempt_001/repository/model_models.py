from typing import Dict, Any

class TextGenerationRequest:
    def __init__(self, prompt: str, model_id: str = "gemini-1.5-flash-001", **kwargs):
        self.prompt = prompt
        self.model_id = model_id
        self.kwargs = kwargs

    def to_vertex_ai_params(self) -> Dict[str, Any]:
        params = {
            "prompt": self.prompt,
            "model_id": self.model_id,
        }
        params.update(self.kwargs)
        return params

class TextGenerationResponse:
    def __init__(self, text: str):
        self.text = text

    @classmethod
    def from_vertex_ai_response(cls, response: Any):
        # Assuming Vertex AI TextGenerationResponse has a .text attribute or similar
        # This might need adjustment based on the actual Vertex AI response structure
        # For now, let's assume it's directly accessible
        return cls(text=response.text)

class StructuredExtractionRequest(TextGenerationRequest):
    def __init__(self, prompt: str, schema: Dict, model_id: str = "gemini-1.5-flash-001", **kwargs):
        super().__init__(prompt, model_id, **kwargs)
        self.schema = schema

    def to_vertex_ai_params(self) -> Dict[str, Any]:
        params = super().to_vertex_ai_params()
        params["schema"] = self.schema  # Add schema for structured extraction
        return params

class StructuredExtractionResponse:
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    @classmethod
    def from_vertex_ai_response(cls, response: Any):
        # Assuming Vertex AI response for structured extraction returns a dict
        return cls(data=response.json() if hasattr(response, 'json') else response)
