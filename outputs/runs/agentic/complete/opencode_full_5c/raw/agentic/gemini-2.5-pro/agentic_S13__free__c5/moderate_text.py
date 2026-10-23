from safety_client import get_openai_client
from safety_models import OpenAIModerationResponse


def moderate_text(text: str) -> OpenAIModerationResponse:
    """
    Scores user text for unsafe content using OpenAI's Moderation API.
    """
    client = get_openai_client()
    response = client.moderations.create(input=text)

    # The response from the client is already a pydantic model,
    # but we are using our own for demonstration and potential extension.
    return OpenAIModerationResponse.model_validate(response.model_dump())
