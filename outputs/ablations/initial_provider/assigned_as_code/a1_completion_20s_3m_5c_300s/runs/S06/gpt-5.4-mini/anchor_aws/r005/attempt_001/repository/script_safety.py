import boto3


def script_safety(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    response = client.detect_sensitive_information(Text=payload["text"], LanguageCode=config.get("language_code", "en"))
    return {"entities": response.get("Entities", []), "is_safe": not response.get("Entities")}
