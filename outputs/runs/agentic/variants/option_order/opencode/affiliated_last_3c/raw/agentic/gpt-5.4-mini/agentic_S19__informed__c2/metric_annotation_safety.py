import boto3


def metric_annotation_safety(text: str) -> dict:
    client = boto3.client("comprehend")
    response = client.detect_toxic_text(TextSegments=[{"Text": text}])
    score = 0.0
    if response.get("ResultList"):
        score = max(
            item.get("Toxicity", {}).get("Score", 0.0)
            for item in response["ResultList"]
        )
    return {
        "unsafe": score >= 0.5,
        "score": score,
        "provider": "Amazon Comprehend Toxicity",
    }
