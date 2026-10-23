import dataclasses
from typing import Any, Dict, List, Optional

@dataclasses.dataclass
class InferenceRequest:
    prompt: str
    model_id: str
    temperature: float = 0.7
    max_output_tokens: int = 1024

@dataclasses.dataclass
class InferenceResponse:
    text: str
    safety_attributes: Optional[Dict[str, Any]] = None

@dataclasses.dataclass
class EmbeddingRequest:
    text_entries: List[str]
    model_id: str

@dataclasses.dataclass
class EmbeddingResponse:
    embeddings: List[List[float]]


def normalize_vertex_ai_response(response: Any) -> InferenceResponse:
    """Normalizes a Vertex AI text generation response."""
    if response.predictions:
        # Assuming the first prediction contains the text
        text_content = response.predictions[0]["content"]
        safety_attributes = response.predictions[0].get("safetyAttributes")
        return InferenceResponse(text=text_content, safety_attributes=safety_attributes)
    return InferenceResponse(text="")

def normalize_vertex_ai_embedding_response(response: Any) -> EmbeddingResponse:
    """Normalizes a Vertex AI embedding response."""
    embeddings = []
    for prediction in response.predictions:
        if "embeddings" in prediction and "values" in prediction["embeddings"]:
            embeddings.append(prediction["embeddings"]["values"])
    return EmbeddingResponse(embeddings=embeddings)
