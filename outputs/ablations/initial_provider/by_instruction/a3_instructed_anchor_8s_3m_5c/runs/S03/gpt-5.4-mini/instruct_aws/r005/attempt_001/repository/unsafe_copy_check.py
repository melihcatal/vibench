import boto3


def unsafe_copy_check(localized_copy):
    client = boto3.client("comprehend", region_name="us-east-1")
    response = client.detect_pii_entities(Text=localized_copy, LanguageCode="en")
    return {"provider": "aws.comprehend", "unsafe": bool(response.get("Entities")), "entities": response.get("Entities", [])}
