from safety_models import RedactionRequest, RedactionResponse
from safety_client import get_content_safety_client
from azure.ai.contentsafety.models import AnalyzeTextOptions


def redact_unsafe(request: RedactionRequest) -> RedactionResponse:
    client = get_content_safety_client()
    request_body = AnalyzeTextOptions(
        text=request.text, output_type="TwoBase64EncodedJson"
    )  # Request with output type for sensitive content
    response = client.analyze_text(request_body)

    redacted_text = list(
        request.text
    )  # Convert to list for mutable character replacement

    if (
        response.hate_result
        and response.hate_result.severity > 0
        and response.hate_result.detection_result.spans
    ):
        for span in response.hate_result.detection_result.spans:
            for i in range(span.offset, span.offset + span.length):
                redacted_text[i] = "*"

    if (
        response.self_harm_result
        and response.self_harm_result.severity > 0
        and response.self_harm_result.detection_result.spans
    ):
        for span in response.self_harm_result.detection_result.spans:
            for i in range(span.offset, span.offset + span.length):
                redacted_text[i] = "*"

    if (
        response.sexual_result
        and response.sexual_result.severity > 0
        and response.sexual_result.detection_result.spans
    ):
        for span in response.sexual_result.detection_result.spans:
            for i in range(span.offset, span.offset + span.length):
                redacted_text[i] = "*"

    if (
        response.violence_result
        and response.violence_result.severity > 0
        and response.violence_result.detection_result.spans
    ):
        for span in response.violence_result.detection_result.spans:
            for i in range(span.offset, span.offset + span.length):
                redacted_text[i] = "*"

    return RedactionResponse(redacted_text="".join(redacted_text))
