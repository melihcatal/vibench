from safety_models import ModerationRequest, ModerationResponse
from safety_client import moderate_text_with_gcp


def moderate_text(text: str) -> ModerationResponse:
    """Scores user text for unsafe or policy-violating content using Google Cloud Natural Language API."""
    request = ModerationRequest(text=text)
    response = moderate_text_with_gcp(request)
    return response
