from safety_client import SafetyClient
from safety_models import ModerationRequest, ModerationResponse, SafetyAttribute

REDaction_PLACEHOLDER = "[REDACTED_UNSAFE_CONTENT]"

def redact_unsafe(text: str) -> str:
    client = SafetyClient()
    moderation_response = client.moderate_text(ModerationRequest(text_content=text))

    if moderation_response.results:
        for result in moderation_response.results:
            if result.blocked:
                return REDaction_PLACEHOLDER
    return text
