from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class ModelGenerationRequest:
    prompt: str
    model_id: str
    temperature: float = 0.7
    max_output_tokens: int = 1024

@dataclass
class ModelGenerationResponse:
    text: str
    finish_reason: Optional[str] = None
    safety_ratings: Optional[List[Dict[str, Any]]] = None
    usage_metadata: Optional[Dict[str, Any]] = None
    raw_response: Optional[Any] = None # To hold the original provider response object

@dataclass
class ModerationRequest:
    text_content: str
    language: str = "en"

@dataclass
class ModerationResponse:
    is_safe: bool
    moderation_scores: Dict[str, float]
    raw_response: Optional[Any] = None


if __name__ == '__main__':
    # Example usage
    # req = ModelGenerationRequest(prompt="Generate a poem.", model_id="gemini-pro")
    # print(req)
    # resp = ModelGenerationResponse(text="A poem about code.", finish_reason="STOP")
    # print(resp)
    pass
