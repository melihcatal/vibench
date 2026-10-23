import boto3

AWS_REGION = "us-west-2"


def redact_unsafe(text):
    comprehend = boto3.client("comprehend", region_name=AWS_REGION)
    response = comprehend.detect_toxic_content(
        TextSegments=[{"Text": text, "ToxicityThreshold": 0.5}], LanguageCode="en"
    )
    redacted_text = text
    for segment in response["ResultList"][0]["ToxicContentList"]:
        redacted_text = (
            redacted_text[: segment["BeginOffset"]]
            + "[REDACTED]"
            + redacted_text[segment["EndOffset"] :]
        )
    return redacted_text
