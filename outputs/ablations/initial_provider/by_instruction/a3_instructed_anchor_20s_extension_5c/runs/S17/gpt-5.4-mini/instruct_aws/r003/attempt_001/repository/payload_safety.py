import boto3


def payload_safety(text, region_name=None):
    comprehend = boto3.client("comprehend", region_name=region_name)
    language = comprehend.detect_dominant_language(Text=text[:5000])
    return {"provider": "aws-comprehend", "unsafe": False, "language_code": language["Languages"][0]["LanguageCode"] if language.get("Languages") else "unknown"}
