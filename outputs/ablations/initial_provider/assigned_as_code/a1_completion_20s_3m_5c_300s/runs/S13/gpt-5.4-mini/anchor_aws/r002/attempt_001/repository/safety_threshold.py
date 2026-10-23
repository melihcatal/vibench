import boto3


def safety_threshold(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region", "us-east-1"))
    response = client.detect_toxic_content(TextSegments=[{"Text": payload["text"]}], LanguageCode="en")
    thresholds = config.get("thresholds", {"toxicity": 0.5})
    score = response["ResultList"][0]["Toxicity"]
    return {"allowed": score < thresholds.get("toxicity", 0.5), "toxicity": score}
