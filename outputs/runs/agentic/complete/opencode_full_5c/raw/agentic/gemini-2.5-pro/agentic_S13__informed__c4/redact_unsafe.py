from typing import List
from azure.ai.contentsafety.models import AnalyzeTextOptions
from safety_client import get_safety_client
from safety_models import RedactionResult


# Note: Assumes a blocklist named 'default' is configured in the Azure AI Content Safety resource.
def redact_unsafe(text: str, blocklist_names: List[str] = None) -> RedactionResult:
    if blocklist_names is None:
        blocklist_names = ["default"]

    client = get_safety_client()

    request = AnalyzeTextOptions(
        text=text, blocklist_names=blocklist_names, break_by_blocklists=True
    )

    try:
        response = client.analyze_text(request)
    except Exception:
        return RedactionResult(redacted_text=text, blocklist_matches=[])

    redacted_text = text
    matches = []
    if response.blocklists_match_results:
        for match in response.blocklists_match_results:
            matches.append(
                {"blocklist_name": match.blocklist_name, "hit_text": match.hit_text}
            )
            redacted_text = redacted_text.replace(match.hit_text, "[REDACTED]")

    return RedactionResult(redacted_text=redacted_text, blocklist_matches=matches)
