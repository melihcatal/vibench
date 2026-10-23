import boto3


def redact_unsafe(text):
    comprehend = boto3.client("comprehend")
    response = comprehend.detect_toxic_content(
        TextSegments=[{"Text": text}], LanguageCode="en"
    )
    redacted_text = text
    for segment in response["ResultList"][0]["ToxicContentList"]:
        redacted_text = (
            redacted_text[: segment["BeginOffset"]]
            + "*" * (segment["EndOffset"] - segment["BeginOffset"])
            + redacted_text[segment["EndOffset"] :]
        )
    return redacted_text
