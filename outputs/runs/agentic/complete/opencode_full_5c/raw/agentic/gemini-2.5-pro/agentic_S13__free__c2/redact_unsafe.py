import boto3
from typing import List, Dict

from safety_client import get_comprehend_client
from safety_models import RedactionResponse


def redact_unsafe(text: str, language_code: str = "en") -> RedactionResponse:
    """
    Detects and redacts toxic content spans from text using AWS Comprehend.
    """
    client = get_comprehend_client()

    # Detect toxic content
    response = client.detect_toxic_content(
        TextSegments=[{"Text": text}], LanguageCode=language_code
    )

    toxic_spans = []
    redacted_text = list(text)

    for label in response["ResultList"][0]["Labels"]:
        score = label["Score"]
        for span in label["Positions"]:
            begin_offset = span["BeginOffset"]
            end_offset = span["EndOffset"]

            toxic_spans.append(
                {"begin_offset": begin_offset, "end_offset": end_offset, "score": score}
            )

            for i in range(begin_offset, end_offset):
                redacted_text[i] = "*"

    return RedactionResponse(
        redacted_text="".join(redacted_text), toxic_spans=toxic_spans
    )
