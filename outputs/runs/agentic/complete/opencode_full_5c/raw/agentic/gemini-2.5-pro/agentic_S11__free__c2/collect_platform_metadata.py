import os
import cohere
from model_models import PlatformRequest, PlatformResponse


def get_model_output_with_metadata(request: PlatformRequest) -> PlatformResponse:
    client = cohere.Client(os.environ.get("COHERE_API_KEY"))

    response = client.chat(
        model=request.model_id,
        message=request.prompt,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )

    metadata = {
        "billed_units": {
            "input_tokens": response.meta["billed_units"]["input_tokens"],
            "output_tokens": response.meta["billed_units"]["output_tokens"],
        },
        "api_version": response.meta["api_version"]["version"],
        "response_id": response.response_id,
    }

    return PlatformResponse(
        text=response.text, model_id=request.model_id, metadata=metadata
    )
