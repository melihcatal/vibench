import os
from safety_client import SafetyClient
from safety_models import ModerationRequest, ModerationResponse

def moderate_text(user_text: str):
    """Score a single user text for unsafe or policy‑violating content using Azure AI Content Safety.
    Returns a boolean indicating if the text is unsafe.
    """
    client = SafetyClient()
    request = ModerationRequest(text=user_text)
    response: ModerationResponse = client.check_content(request)
    # Treat any flag with severity >= warning as unsafe
    unsafe = any(flag.severity >= flag.WARNING for flag in response.flags)
    return unsafe
