from typing import Dict, Any, List

def create_generation_request(prompt: str, temperature: float = 0.7, max_output_tokens: int = 1024) -> Dict[str, Any]:
    """Creates a standardized model generation request payload."""
    return {
        "prompt": prompt,
        "temperature": temperature,
        "max_output_tokens": max_output_tokens,
    }

def normalize_generation_response(raw_response: Any) -> Dict[str, Any]:
    """Normalizes a raw model generation response into a standard format."
    # Assuming raw_response is a vertexai.language_models.TextGenerationResponse object
    normalized_data = {
        "generated_text": raw_response.text if hasattr(raw_response, 'text') else str(raw_response),
        "safety_attributes": raw_response.safety_attributes.to_dict() if hasattr(raw_response, 'safety_attributes') and raw_response.safety_attributes else None,
        "citation_metadata": [
            citation.to_dict() for citation in raw_response.citation_metadata.citations
        ] if hasattr(raw_response, 'citation_metadata') and raw_response.citation_metadata else [],
        # Add other relevant fields as needed
    }
    return normalized_data


def create_embedding_request(texts: List[str]) -> Dict[str, Any]:
    """Creates a standardized embedding request payload."""
    return {
        "texts": texts
    }
