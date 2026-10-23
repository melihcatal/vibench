from azure.ai.contentsafety.models import AnalyzeTextOptions
from azure.core.exceptions import HttpResponseError

from safety_client import get_safety_client

def redact_unsafe(text: str, blocklist_name: str, redaction_char: str = "*") -> str:
    """
    Redacts text based on matches from a custom blocklist in Azure AI Content Safety.

    Args:
        text: The input text.
        blocklist_name: The name of the blocklist to use for redaction.
        redaction_char: The character to use for redaction.

    Returns:
        The text with matched terms redacted.
    """
    client = get_safety_client()
    request = AnalyzeTextOptions(text=text, blocklist_names=[blocklist_name], break_by_blocklists=True)

    try:
        response = client.analyze_text(request)
    except HttpResponseError as e:
        print(f"Error during redaction analysis: {e}")
        return text # Return original text on error

    if not response.blocklists_match:
        return text

    # Convert to list for mutation
    text_list = list(text)
    for match in response.blocklists_match:
        start = match.offset
        end = start + match.length
        text_list[start:end] = [redaction_char] * match.length
    
    return "".join(text_list)
