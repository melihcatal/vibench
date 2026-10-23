import os
from typing import Dict, Any, Tuple
import cohere
from model_models import PlatformRequest

def invoke_and_collect_metadata(request: PlatformRequest) -> Tuple[str, Dict[str, Any]]:
    """
    Invokes a Cohere model and returns its output along with platform metadata.

    Returns:
        A tuple containing the generated text and a dictionary of metadata.
    """
    client = cohere.Client(os.environ.get("COHERE_API_KEY"))
    
    response = client.chat(
        model=request.model_id,
        message=request.prompt,
        max_tokens=request.max_tokens,
    )
    
    metadata = {
        "api_version": response.meta.api_version,
        "billed_units": {
            "input_tokens": response.meta.billed_units.input_tokens,
            "output_tokens": response.meta.billed_units.output_tokens,
        } if response.meta.billed_units else None,
        "finish_reason": response.finish_reason,
        "response_id": response.response_id,
    }
    
    return response.text, metadata
