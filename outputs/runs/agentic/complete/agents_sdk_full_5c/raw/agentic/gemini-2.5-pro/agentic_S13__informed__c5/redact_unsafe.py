from safety_client import get_safety_client
from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.exceptions import HttpResponseError

def redact_unsafe(text: str, blocklist_name: str, redaction_char: str = "*") -> str:
    """
    Redacts unsafe spans from text based on a pre-defined server blocklist.
    """
    client = get_safety_client()

    request = AnalyzeTextOptions(text=text, blocklist_names=[blocklist_name])
    
    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Analyze text with blocklist failed: {e.message}")
        return text

    if not response.blocklists_match:
        return text

    # Create a list of characters to allow for modification
    text_list = list(text)
    
    for match in response.blocklists_match:
        offset = match.offset
        length = match.length
        # Replace the matched span with the redaction character
        for i in range(offset, offset + length):
            if i < len(text_list):
                text_list[i] = redaction_char

    return "".join(text_list)
