from azure.ai.contentsafety.models import AnalyzeTextOptions
from safety_client import get_azure_content_safety_client
from safety_models import RedactionResult


def redact_unsafe(text: str) -> RedactionResult:
    client = get_azure_content_safety_client()

    request = AnalyzeTextOptions(text=text)

    try:
        response = client.analyze_text(request)
    except Exception as e:
        print(f"Error analyzing text with Azure Content Safety: {e}")
        return RedactionResult(
            original_text=text, redacted_text=text, redactions_found=0
        )

    redacted_text_list = list(text)
    redactions_found = 0

    if response.hate_result and response.hate_result.blocklists_match:
        for match in response.hate_result.blocklists_match:
            offset = match.offset
            length = match.length
            redacted_text_list[offset : offset + length] = ["[REDACTED]"] * length
            redactions_found += 1

    return RedactionResult(
        original_text=text,
        redacted_text="".join(redacted_text_list),
        redactions_found=redactions_found,
    )
