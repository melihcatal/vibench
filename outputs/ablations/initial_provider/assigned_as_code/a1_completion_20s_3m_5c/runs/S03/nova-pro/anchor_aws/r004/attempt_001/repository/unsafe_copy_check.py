import boto3


def check_unsafe_content(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    text = payload["text"]
    response = client.detect_toxic_content(
        TextSegments=[{"Text": text}],
        LanguageCode=payload["language_code"],
    )
    return {
        "toxic_content_detected": response["Results"][0]["ToxicContentDetected"],
    }