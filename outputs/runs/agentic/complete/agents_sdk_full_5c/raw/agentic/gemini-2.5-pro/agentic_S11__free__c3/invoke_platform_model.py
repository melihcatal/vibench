import os
import cohere
from model_models import PlatformRequest, PlatformResponse

def invoke_model(request: PlatformRequest) -> PlatformResponse:
    """Invokes a Cohere model with the given request."""
    client = cohere.Client(os.environ.get("COHERE_API_KEY"))
    
    response = client.chat(
        model=request.model_id,
        message=request.prompt,
        max_tokens=request.max_tokens,
    )
    
    return PlatformResponse(
        text=response.text,
        model_id=request.model_id
    )
