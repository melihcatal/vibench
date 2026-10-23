from safety_client import get_safety_client
from azure.ai.contentsafety.models import AnalyzeTextOptions
from safety_models import RedactionResult

def redact_unsafe(text: str, blocklist_name: str) -> RedactionResult:
    """
    Analyzes text against a custom blocklist and redacts matched terms.

    This function relies on a pre-existing named blocklist on the
    Azure AI Content Safety service.

    :param text: The input text.
    :param blocklist_name: The name of the blocklist to check against.
    :return: A RedactionResult containing the original and redacted text.
    """
    client = get_safety_client()
    
    # AnalyzeText can check against pre-configured blocklists by name
    request = AnalyzeTextOptions(text=text, blocklist_names=[blocklist_name])
    
    try:
        response = client.analyze_text(request)
    except Exception:
        # If the service call fails, return the original text without redactions
        return RedactionResult(original_text=text, redacted_text=text, was_redacted=False, hits=[])

    redacted_text = text
    hits = []
    if response.blocklists_match:
        for match in response.blocklists_match:
            hits.append(match.blocklist_name)
            redacted_text = redacted_text.replace(match.text, "*" * len(match.text))
            
    was_redacted = text != redacted_text
    
    return RedactionResult(
        original_text=text,
        redacted_text=redacted_text,
        was_redacted=was_redacted,
        hits=list(set(hits)) # Unique blocklist names that were hit
    )
