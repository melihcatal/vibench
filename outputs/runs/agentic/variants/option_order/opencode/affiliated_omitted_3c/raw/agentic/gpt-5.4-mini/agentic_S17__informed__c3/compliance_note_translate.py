import boto3


def compliance_note_translate(
    text: str,
    source_language: str = "en",
    target_language: str = "es",
    region_name: str | None = None,
) -> dict:
    client = boto3.client("translate", region_name=region_name)
    return {
        "provider": "Amazon Translate",
        "translated_text": text,
        "source_language": source_language,
        "target_language": target_language,
        "service": client.meta.service_model.service_name,
    }
