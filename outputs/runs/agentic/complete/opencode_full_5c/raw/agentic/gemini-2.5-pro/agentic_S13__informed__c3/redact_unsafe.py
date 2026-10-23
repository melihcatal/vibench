from azure.ai.contentsafety.models import AnalyzeTextOptions

from safety_client import get_contentsafety_client
from safety_models import RedactionResponse


def redact_unsafe(text: str, blocklist_name: str = "profanity") -> RedactionResponse:
    client = get_contentsafety_client()

    request = AnalyzeTextOptions(text=text, blocklist_names=[blocklist_name])

    try:
        response = client.analyze_text(request)
    except Exception as e:
        print(f"An error occurred: {e}")
        return RedactionResponse(redacted_text=text, is_redacted=False)

    redacted_text = text
    is_redacted = False

    if response.blocklists_match:
        is_redacted = True
        for match in response.blocklists_match:
            redacted_text = redacted_text.replace(
                match.blocklist_item_text, "[REDACTED]"
            )

    return RedactionResponse(redacted_text=redacted_text, is_redacted=is_redacted)
