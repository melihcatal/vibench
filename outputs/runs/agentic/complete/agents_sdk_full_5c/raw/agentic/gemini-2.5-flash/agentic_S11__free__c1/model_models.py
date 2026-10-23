from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class ModelInput:
    prompt: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    
@dataclass
class ModelOutputPart:
    text: Optional[str] = None
    # Add other part types if needed, e.g., inline_data, file_data

@dataclass
class ModelOutputCandidate:
    parts: List[ModelOutputPart] = field(default_factory=list)
    safety_attributes: Optional[Dict[str, Any]] = None # Placeholder for safety scores

@dataclass
class PlatformModelOutput:
    generated_content: Optional[str] = None
    candidates: List[ModelOutputCandidate] = field(default_factory=list)
    usage_metadata: Dict[str, Any] = field(default_factory=dict)
    raw_response: Optional[Dict[str, Any]] = None
    model_id: Optional[str] = None
    
def normalize_vertex_ai_response(raw_response: Dict[str, Any], model_id: str) -> PlatformModelOutput:
    """Normalizes a raw Vertex AI PredictionService response into a common PlatformModelOutput structure."""
    generated_content = ""
    candidates: List[ModelOutputCandidate] = []
    usage_metadata: Dict[str, Any] = {}

    if 'predictions' in raw_response and raw_response['predictions']:
        for pred in raw_response['predictions']:
            if isinstance(pred, dict) and 'candidates' in pred:
                for candidate_raw in pred['candidates']:
                    parts: List[ModelOutputPart] = []
                    if 'content' in candidate_raw and 'parts' in candidate_raw['content']:
                        for part_raw in candidate_raw['content']['parts']:
                            if 'text' in part_raw:
                                parts.append(ModelOutputPart(text=part_raw['text']))
                                generated_content += part_raw['text'] # Accumulate text
                    
                    safety_attributes = None
                    if 'safetyAttributes' in candidate_raw:
                        safety_attributes = candidate_raw['safetyAttributes']
                        
                    candidates.append(ModelOutputCandidate(parts=parts, safety_attributes=safety_attributes))
            elif isinstance(pred, str):
                generated_content += pred # Handle simpler string responses
                candidates.append(ModelOutputCandidate(parts=[ModelOutputPart(text=pred)]))
    
    # Extract usage metadata if available (e.g., for generative models)
    if 'metadata' in raw_response and 'tokenMetadata' in raw_response['metadata']:
        token_meta = raw_response['metadata']['tokenMetadata']
        if 'inputTokenCount' in token_meta:
            usage_metadata["input_token_count"] = token_meta['inputTokenCount']
        if 'outputTokenCount' in token_meta:
            usage_metadata["output_token_count"] = token_meta['outputTokenCount']

    return PlatformModelOutput(
        generated_content=generated_content.strip(),
        candidates=candidates,
        usage_metadata=usage_metadata,
        raw_response=raw_response,
        model_id=model_id
    )

if __name__ == '__main__':
    # Example usage for normalization
    sample_raw_vertex_response = {
        "predictions": [
            {
                "candidates": [
                    {
                        "content": {
                            "parts": [
                                {"text": "Hello"},
                                {"text": " World!"}
                            ]
                        },
                        "safetyAttributes": {"categories": ["HARM_CATEGORY_DANGEROUS"], "scores": [0.9]}
                    }
                ]
            }
        ],
        "metadata": {"tokenMetadata": {"inputTokenCount": 5, "outputTokenCount": 2}}
    }

    normalized_output = normalize_vertex_ai_response(sample_raw_vertex_response, "gemini-pro")
    print("Normalized Output:", normalized_output.generated_content)
    print("Usage Metadata:", normalized_output.usage_metadata)
    if normalized_output.candidates:
        print("First candidate safety attributes:", normalized_output.candidates[0].safety_attributes)
