from typing import List
from security_client import SecurityClientConfig
from security_models import PIIEntity

def check_payload_for_unsafe_content(text_payload: str) -> List[PIIEntity]:
    comprehend_client = SecurityClientConfig.get_comprehend_client()

    response = comprehend_client.detect_pii_entities(
        Text=text_payload,
        LanguageCode='en'
    )

    pii_entities = []
    for entity in response.get('Entities', []):
        pii_entities.append(
            PIIEntity(
                score=entity["Score"],
                type=entity["Type"],
                begin_offset=entity["BeginOffset"],
                end_offset=entity["EndOffset"],
                text=text_payload[entity["BeginOffset"]:entity["EndOffset"]]
            )
        )
    
    return pii_entities