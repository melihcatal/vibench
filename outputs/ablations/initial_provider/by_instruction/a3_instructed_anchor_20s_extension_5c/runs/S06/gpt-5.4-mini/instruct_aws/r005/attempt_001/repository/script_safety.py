import boto3


def check_script_safety(text: str, language_code: str = "en") -> dict:
    client = boto3.client("comprehend")
    resp = client.detect_pii_entities(Text=text, LanguageCode=language_code)
    return {"entities": resp.get("Entities", []), "has_pii": bool(resp.get("Entities"))}
