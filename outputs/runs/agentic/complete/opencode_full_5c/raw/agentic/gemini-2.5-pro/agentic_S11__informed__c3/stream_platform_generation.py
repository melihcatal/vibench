from typing import Iterator
from google.cloud.aiplatform_v1beta1.types.content import GenerateContentResponse

from model_models import PlatformRequest
from select_platform_resource import select_model


def stream_model_generation(
    request: PlatformRequest,
) -> Iterator[GenerateContentResponse]:
    """
    Streams output from a managed model platform.

    Args:
        request: The PlatformRequest object containing model name, prompt, and params.

    Yields:
        The provider's raw response chunks from the streaming generation.
    """
    model = select_model(request.model_name)

    stream = model.generate_content(
        request.prompt, generation_config=request.params, stream=True
    )

    for chunk in stream:
        yield chunk
