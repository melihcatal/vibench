import boto3


def vendor_text_safety(text):
    client = boto3.client("comprehend", region_name="us-east-1")
    response = client.detect_pii_entities(Text=text[:4500], LanguageCode="en")
    return {"redacted": text, "entities": response.get("Entities", [])}
