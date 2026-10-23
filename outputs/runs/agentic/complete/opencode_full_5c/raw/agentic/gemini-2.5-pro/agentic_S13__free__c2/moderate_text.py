from safety_client import get_openai_client
from safety_models import ModerationResponse


def moderate_text(text: str) -> ModerationResponse:
    """
    Scores user text for unsafe or policy-violating content using OpenAI's Moderation API.
    """
    client = get_openai_client()
    response = client.moderations.create(input=text, model="text-moderation-latest")

    return ModerationResponse.model_validate(response.dict())
