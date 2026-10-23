import os
from typing import List
from azure.ai.contentsafety.models import AnalyzeTextOptions
from safety_client import get_azure_content_safety_client
from safety_models import ModerationCategory, ModerationResult

def redact_unsafe(text: str, blocklist_names: List[str] = None) -> ModerationResult:
    client = get_azure_content_safety_client()
    
    if blocklist_names is None:
        blocklist_names = [os.environ.get("AZURE_CONTENT_SAFETY_DEFAULT_BLOCKLIST", "my_default_blocklist")]

    request = AnalyzeTextOptions(text=text, blocklists=blocklist_names)
    response = client.analyze_text(request)

    categories = []
    overall_decision = "Safe"

    if response.hate_result:
        categories.append(ModerationCategory(category="Hate", severity=response.hate_result.severity, violates=response.hate_result.severity > 0))
        if response.hate_result.severity > 0:
            overall_decision = "Unsafe"
    if response.self_harm_result:
        categories.append(ModerationCategory(category="SelfHarm", severity=response.self_harm_result.severity, violates=response.self_harm_result.severity > 0))
        if response.self_harm_result.severity > 0:
            overall_decision = "Unsafe"
    if response.sexual_result:
        categories.append(ModerationCategory(category="Sexual", severity=response.sexual_result.severity, violates=response.sexual_result.severity > 0))
        if response.sexual_result.severity > 0:
            overall_decision = "Unsafe"
    if response.violence_result:
        categories.append(ModerationCategory(category="Violence", severity=response.violence_result.severity, violates=response.violence_result.severity > 0))
        if response.violence_result.severity > 0:
            overall_decision = "Unsafe"

    redacted_text = text
    if response.blocklists_match_results:
        sorted_matches = sorted(response.blocklists_match_results, key=lambda m: m.offset, reverse=True)
        for match in sorted_matches:
            match_length = len(match.text)
            start_index = match.offset
            end_index = start_index + match_length
            redacted_text = redacted_text[:start_index] + "*" * match_length + redacted_text[end_index:]
    
    if overall_decision == "Unsafe" and not response.blocklists_match_results:
        redacted_text = "[REDACTED_UNSAFE_CONTENT]"

    return ModerationResult(
        text=text,
        categories=categories,
        overall_decision=overall_decision,
        redacted_text=redacted_text,
        raw_response=response.as_dict()
    )
