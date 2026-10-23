import boto3


def moderate_batch(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region", "us-east-1"))
    texts = payload.get("messages", [])
    segments = [{"Text": item.get("text", "")} for item in texts]
    response = client.detect_toxic_content(TextSegments=segments, LanguageCode="en")
    results = []
    for item, result in zip(texts, response.get("ResultList", [])):
        results.append({"id": item.get("id"), "text": item.get("text", ""), "toxicity": result.get("Toxicity")})
    return {"results": results}
