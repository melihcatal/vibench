import boto3


def moderate_text(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region", "us-east-1"))
    response = client.detect_toxic_content(TextSegments=[{"Text": payload["text"]}], LanguageCode="en")
    return {"toxicity": response["ResultList"][0]["Toxicity"]}
