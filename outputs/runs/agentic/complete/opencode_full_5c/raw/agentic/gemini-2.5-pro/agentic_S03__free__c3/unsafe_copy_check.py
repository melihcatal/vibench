from translation_client import openai_client
from translation_models import UnsafeCopyCheckRequest, UnsafeCopyCheckResponse


def unsafe_copy_check(request: UnsafeCopyCheckRequest) -> UnsafeCopyCheckResponse:
    """
    Checks for unsafe content using OpenAI's Moderation API.
    """
    response = openai_client.moderations.create(input=request.text)
    result = response.results[0]

    is_unsafe = result.flagged
    details = result.categories.dict()

    return UnsafeCopyCheckResponse(is_unsafe=is_unsafe, details=details)
