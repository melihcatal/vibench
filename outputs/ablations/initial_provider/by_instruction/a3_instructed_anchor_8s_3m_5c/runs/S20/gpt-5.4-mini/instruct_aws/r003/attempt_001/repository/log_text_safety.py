import boto3


def check_log_text_safety(text: str) -> dict:
    client = boto3.client("comprehend")
    response = client.detect_pii_entities(Text=text, LanguageCode="en")
    return {"entities": response.get("Entities", []), "unsafe": bool(response.get("Entities"))}


if __name__ == "__main__":
    check_log_text_safety("sample")
