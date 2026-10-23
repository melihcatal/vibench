from typing import List, Dict, Any
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.exceptions import HttpResponseError

from safety_client import get_azure_safety_client


def redact_unsafe(text: str, blocklist_names: List[str]) -> Dict[str, Any]:
    """
    Flags text from custom blocklists. Azure Content Safety identifies matches
    and their offsets, which can be used for redaction.
    
    This function returns the raw blocklist match information.
    """
    client = get_azure_safety_client()
    
    # Note: You must have pre-configured a blocklist in your Azure resource.
    # If blocklist_names is empty, the service will not check against any blocklist.
    if not blocklist_names:
        return {"flagged": False, "blocklist_matches": []}

    request = AnalyzeTextOptions(text=text, blocklist_names=blocklist_names)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text with blocklist failed. Reason: {e.reason}")
        # Depending on policy, might fail open or closed.
        return {"flagged": True, "error": str(e)}

    flagged = bool(response.blocklists_match)
    
    return {
        "flagged": flagged,
        "blocklist_matches": [match.to_dict() for match in response.blocklists_match]
    }
