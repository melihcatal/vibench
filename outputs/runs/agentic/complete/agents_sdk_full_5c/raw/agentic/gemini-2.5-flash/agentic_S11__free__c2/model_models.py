from typing import Dict, Any, List, Optional

class PlatformGenerationRequest:
    """Local representation of a model generation request."""
    def __init__(self, prompt: str, model_id: str, parameters: Optional[Dict[str, Any]] = None):
        self.prompt = prompt
        self.model_id = model_id
        self.parameters = parameters if parameters is not None else {}

class PlatformGenerationResponse:
    """Local representation of a normalized model generation response."""
    def __init__(self, generated_text: str, model_id: str, raw_response: Any, metadata: Optional[Dict[str, Any]] = None):
        self.generated_text = generated_text
        self.model_id = model_id
        self.raw_response = raw_response
        self.metadata = metadata if metadata is not None else {}

    @classmethod
    def from_vertex_ai_response(cls, model_id: str, response: Any):
        metadata = {
            "citation_metadata": response.citation_metadata.to_dict() if response.citation_metadata else None,
            "safety_attributes": response.safety_attributes.to_dict() if response.safety_attributes else None,
        }
        return cls(generated_text=response.text, model_id=model_id, raw_response=response, metadata=metadata)

class PlatformEmbeddingResponse:
    """Local representation of a normalized model embedding response."""
    def __init__(self, embeddings: List[List[float]], model_id: str, raw_response: Any, metadata: Optional[Dict[str, Any]] = None):
        self.embeddings = embeddings
        self.model_id = model_id
        self.raw_response = raw_response
        self.metadata = metadata if metadata is not None else {}

    @classmethod
    def from_vertex_ai_response(cls, model_id: str, response: Any):
        embeddings = [embedding.values for embedding in response.embeddings]
        return cls(embeddings=embeddings, model_id=model_id, raw_response=response, metadata={})
