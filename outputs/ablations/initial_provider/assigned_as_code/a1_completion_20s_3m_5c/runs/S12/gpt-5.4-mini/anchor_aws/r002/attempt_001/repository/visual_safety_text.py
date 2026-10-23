import boto3

from vision_client import load_config


def visual_safety_text(payload, config=None):
    config = load_config(config)
    client = boto3.client("comprehend", region_name=config.get("region"))
    text = payload.get("text", "") if isinstance(payload, dict) else ""
    response = client.detect_pii_entities(Text=text, LanguageCode="en")
    entities = [entity["Type"] for entity in response.get("Entities", [])]
    return {"unsafe_text": bool(entities), "entities": entities}
