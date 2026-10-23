from azure.ai.contentsafety.models import AnalyzeTextOptions
from safety_client import get_safety_client
from safety_models import RedactionRequest, RedactionResponse, RedactedSpan


def redact_unsafe(request: RedactionRequest) -> RedactionResponse:
    client = get_safety_client()

    analysis_request = AnalyzeTextOptions(
        text=request.text, blocklist_names=[request.blocklist_name]
    )

    response = client.analyze_text(analysis_request)

    original_text = request.text
    redacted_text = list(original_text)
    flagged_spans = []

    if response.blocklists_match_results:
        for match in response.blocklists_match_results:
            span = RedactedSpan(
                text=match.text, offset=match.offset, length=match.length
            )
            flagged_spans.append(span)

            for i in range(match.offset, match.offset + match.length):
                if i < len(redacted_text):
                    redacted_text[i] = "*"

    return RedactionResponse(
        redacted_text="".join(redacted_text), flagged_spans=flagged_spans
    )
