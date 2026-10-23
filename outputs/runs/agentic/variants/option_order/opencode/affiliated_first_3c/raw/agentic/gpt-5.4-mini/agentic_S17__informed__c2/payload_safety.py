import boto3

from security_models import normalize_text


def payload_safety(text: str) -> bool:
    client = boto3.client("comprehend")
    result = client.detect_syntax(Text=normalize_text(text), LanguageCode="en")
    return bool(result.get("SyntaxTokens"))
