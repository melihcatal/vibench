from typing import Iterator
from vertexai.generative_models import GenerativeModel, Part, GenerationResponse
from model_models import ModelRequest


def stream_model_generation(
    model: GenerativeModel, request: ModelRequest
) -> Iterator[GenerationResponse]:
    """
    Streams output from a managed model platform while preserving provider response objects.

    Args:
        model: The GenerativeModel instance to use.
        request: The request object containing the prompt.

    Yields:
        The provider's response objects as they are generated.
    """
    part = Part.from_text(request.prompt)
    stream = model.generate_content([part], stream=True)
    for chunk in stream:
        yield chunk
