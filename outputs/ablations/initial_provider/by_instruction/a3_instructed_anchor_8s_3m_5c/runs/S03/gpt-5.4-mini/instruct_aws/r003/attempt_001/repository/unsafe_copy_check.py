import boto3


def check_unsafe_copy(text: str, aws_region: str | None = None) -> dict[str, object]:
    comprehend = boto3.client("comprehend", region_name=aws_region)
    pii = comprehend.detect_pii_entities(Text=text, LanguageCode="en")
    return {"provider": "aws-comprehend", "entity_count": len(pii.get("Entities", [])), "entities": pii.get("Entities", [])}
