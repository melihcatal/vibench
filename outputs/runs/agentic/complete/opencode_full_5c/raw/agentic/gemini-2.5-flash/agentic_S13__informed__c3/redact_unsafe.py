from safety_client import analyze_text_with_azure
from safety_models import RedactionRequest, RedactionResponse


def redact_unsafe(request: RedactionRequest) -> RedactionResponse:
    analysis_response = analyze_text_with_azure(request.text)
    redacted_text = list(request.text)
    flagged_spans = []

    # Redact based on blocklist matches if any
    if analysis_response.get("blocklist_matches"):
        for match in analysis_response["blocklist_matches"]:
            start = match["offset"]  # Assuming 'offset' is the start index
            length = len(match["text"])
            for i in range(start, start + length):
                redacted_text[i] = "*"
            flagged_spans.append(
                {"category": "blocklist", "offset": start, "length": length}
            )

    # Optionally redact based on severity thresholds if provided
    if request.thresholds:
        for result in analysis_response["results"]:
            category = result["category"]
            severity = result["severity"]
            if (
                category in request.thresholds
                and severity >= request.thresholds[category]
            ):
                # This is a simplified redaction without specific span information
                # for non-blocklist categories. In a real scenario, more advanced
                # NLP would be needed to identify the exact unsafe spans.
                # For now, we will just flag it.
                flagged_spans.append(
                    {"category": category, "offset": 0, "length": len(request.text)}
                )

    return RedactionResponse(
        redacted_text="".join(redacted_text), flagged_spans=flagged_spans
    )
