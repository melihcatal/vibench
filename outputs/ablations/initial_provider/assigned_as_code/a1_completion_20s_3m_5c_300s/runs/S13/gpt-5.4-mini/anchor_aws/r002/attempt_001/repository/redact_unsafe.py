import boto3


def redact_unsafe(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region", "us-east-1"))
    response = client.detect_toxic_content(TextSegments=[{"Text": payload["text"]}], LanguageCode="en")
    spans = []
    for item in response.get("ResultList", []):
        for label in item.get("Labels", []):
            spans.append({"category": label.get("Name"), "score": label.get("Score")})
    return {"text": payload["text"], "unsafe_spans": spans}
