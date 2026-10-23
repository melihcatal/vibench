from safety_client import get_azure_content_safety_client
from safety_models import RedactUnsafeRequest, RedactUnsafeResponse, RedactedText
from azure.ai.contentsafety.models import AnalyzeTextOptions


def redact_unsafe(request: RedactUnsafeRequest) -> RedactUnsafeResponse:
    client = get_azure_content_safety_client()

    analysis_result = client.analyze_text(AnalyzeTextOptions(text=request.text))

    redacted_text = list(request.text)
    redacted_spans = []

    if (
        analysis_result.hate_result
        and analysis_result.hate_result.blocklists_match_results
    ):
        for match in analysis_result.hate_result.blocklists_match_results:
            offset = match.offset
            length = match.length
            redacted_spans.append((offset, length))
            for i in range(offset, offset + length):
                if i < len(redacted_text):
                    redacted_text[i] = "*"

    return RedactUnsafeResponse(
        redacted_text=RedactedText(
            text="".join(redacted_text),
            redacted_spans=redacted_spans,
        )
    )
