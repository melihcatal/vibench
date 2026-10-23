import boto3


def log_text_safety(text, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    response = client.detect_pii_entities(Text=text, LanguageCode=config.get("language", "en"))
    return {"unsafe": bool(response.get("Entities")), "entities": response.get("Entities", [])}
