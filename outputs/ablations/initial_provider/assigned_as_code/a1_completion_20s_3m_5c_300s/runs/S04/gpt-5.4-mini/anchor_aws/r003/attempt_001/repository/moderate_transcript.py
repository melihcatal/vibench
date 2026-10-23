import boto3


def moderate_transcript(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    text = payload.get("text") or " ".join(segment.get("text", "") for segment in payload.get("segments", []))
    response = client.detect_pii_entities(Text=text, LanguageCode=payload.get("language_code", "en"))
    return {
        "text": text,
        "entities": response.get("Entities", []),
        "job_id": payload.get("job_id"),
    }
