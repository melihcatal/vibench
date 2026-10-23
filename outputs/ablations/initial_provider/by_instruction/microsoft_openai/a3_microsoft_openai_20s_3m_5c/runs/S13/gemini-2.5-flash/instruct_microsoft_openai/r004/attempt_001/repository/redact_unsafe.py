from safety_client import SafetyClient
from safety_models import TextModerationRequest

def redact_unsafe(text: str, threshold: int = 4) -> str:
    client = SafetyClient()
    request = TextModerationRequest(text=text)
    response = client.moderate_text(request)

    is_unsafe = False
    if response.categories:
        for category_result in response.categories:
            if category_result.get("severity", 0) >= threshold:
                is_unsafe = True
                break

    if is_unsafe:
        return "[REDACTED]"
    else:
        return text
