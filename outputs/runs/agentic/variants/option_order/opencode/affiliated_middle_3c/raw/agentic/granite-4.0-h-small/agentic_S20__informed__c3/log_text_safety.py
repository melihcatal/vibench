from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from observability_client import get_content_safety_config


def safe_messages(log_events):
    """
    Check selected log message text for unsafe or toxic content using Azure AI Content Safety.

    Parameters
    ----------
    log_events: list[dict]
        Log entries containing a 'message' field to evaluate.

    Returns
    -------
    list[dict]
        Filtered list preserving the original structure but only retaining messages deemed safe.
    """
    config = get_content_safety_config()
    azure_endpoint = config["endpoint"]
    azure_key = config["key"]
    client = ContentSafetyClient(azure_endpoint, AzureKeyCredential(azure_key))
    safe_events = []
    for ev in log_events:
        message = ev.get("message", "")
        # Call moderation API (text moderation endpoint)
        result = client.analyze_text(content=message)
        # result contains 'categories' with scores; assuming 'safety' score >= 0.9 is safe
        if result.safety_score >= 0.9:
            safe_events.append(ev)
    return safe_events
