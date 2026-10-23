import boto3
from translation_client import get_comprehend_client

def unsafe_copy_check(payload, config=None):
    config = config or {}
    client = get_comprehend_client(region_name=config.get("region"))
    response = client.detect_pii_entities(
        Text=payload["localized_copy"],
        LanguageCode=payload["target_language"],
    )
    pii_entities_found = []
    for entity in response["Entities"]:
        pii_entities_found.append({
            "type": entity["Type"],
            "score": entity["Score"],
            "begin_offset": entity["BeginOffset"],
            "end_offset": entity["EndOffset"],
        })
    return {
        "pii_entities": pii_entities_found,
        "localized_copy": payload["localized_copy"],
        "target_language": payload["target_language"],
    }