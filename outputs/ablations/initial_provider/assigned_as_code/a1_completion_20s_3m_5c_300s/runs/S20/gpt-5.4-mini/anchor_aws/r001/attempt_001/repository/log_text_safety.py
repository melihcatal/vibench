import boto3


def log_text_safety(text, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    response = client.detect_toxic_content(TextSegments=[{"Text": text}], LanguageCode=config.get("language", "en")]
    scores = response.get("ResultList", [])
    unsafe = any(item.get("Toxicity") == "HIGH" for item in scores)
    return {"unsafe": unsafe, "details": scores}
