from safety_client import get_content_safety_client
from safety_models import TextModerationResponse, parse_content_safety_response
from azure.ai.contentsafety.models import AnalyzeTextContentItem


def moderate_text(text: str) -> TextModerationResponse:
    """
    Scores user text for unsafe or policy-violating content using Azure AI Content Safety.
    """
    client = get_content_safety_client()

    request = AnalyzeTextContentItem(text=text)
    response = client.analyze_text(text_item=request)

    return parse_content_safety_response(response.as_dict(), text)
