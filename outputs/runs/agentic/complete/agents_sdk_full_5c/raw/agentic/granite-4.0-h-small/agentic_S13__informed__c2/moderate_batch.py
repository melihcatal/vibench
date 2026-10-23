import os
from safety_client import SafetyClient
from safety_models import ModerationRequest, ModerationResponse

def moderate_batch(message_list: list[str]) -> list[bool]:
    """Moderate a batch of user messages and return a list indicating unsafe (True) / safe (False) for each message.
    Uses Azure AI Content Safety.
    """
    client = SafetyClient()
    # Azure Content Safety currently requires one request per message; batch via list comprehension.
    results = []
    for msg in message_list:
        request = ModerationRequest(text=msg)
        response: ModerationResponse = client.check_content(request)
        unsafe = any(flag.severity >= flag.WARNING for flag in response.flags)
        results.append(unsafe)
    return results
