from typing import Tuple
from model_client import get_vertex_client
from vertexai.generative_models import GenerativeModel
from model_models import (
    PlatformModelRequest,
    PlatformModelResponse,
    PlatformModelMetadata,
)


def get_model_response_with_metadata(
    request: PlatformModelRequest,
) -> Tuple[PlatformModelResponse, PlatformModelMetadata]:
    """
    Gets a model response and its associated metadata from Vertex AI.
    """
    get_vertex_client()

    model = GenerativeModel(request.model_id)

    response = model.generate_content(request.prompt)

    usage_metadata = response.usage_metadata

    platform_response = PlatformModelResponse(text=response.text, raw_response=response)

    platform_metadata = PlatformModelMetadata(
        input_token_count=usage_metadata.prompt_token_count,
        output_token_count=usage_metadata.candidates_token_count,
        raw_metadata=usage_metadata,
    )

    return platform_response, platform_metadata
