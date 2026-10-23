import os
from typing import List, Dict, Any

import boto3

def check_annotation_safety(text: str, language_code: str = 'en') -> Dict[str, Any]:
    comprehend = boto3.client('comprehend')

    response = comprehend.detect_pii_entities(
        Text=text,
        LanguageCode=language_code
    )

    pii_entities = response.get('Entities', [])

    is_safe = not bool(pii_entities)

    return {
        "text": text,
        "is_safe": is_safe,
        "pii_entities_detected": pii_entities
    }
