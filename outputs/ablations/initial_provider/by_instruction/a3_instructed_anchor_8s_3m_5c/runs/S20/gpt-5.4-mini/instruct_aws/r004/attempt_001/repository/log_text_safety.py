import boto3


def check_text(message: str) -> dict:
    client = boto3.client("comprehend")
    response = client.detect_pii_entities(Text=message, LanguageCode="en")
    return {"provider": "aws-comprehend", "unsafe": bool(response.get("Entities")), "entities": response.get("Entities", [])}


if __name__ == "__main__":
    check_text("sample")
