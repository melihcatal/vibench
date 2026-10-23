from google.cloud import language_v1
from typing import Dict, Any, List

def unsafe_copy_check(payload: Dict[str, str], config: Dict[str, Any]) -> Dict[str, Any]:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=payload["translated_text"],
        type_=language_v1.Document.Type.PLAIN_TEXT,
        language=payload["target_language"],
    )

    # This is a basic example; a real-world unsafe content check would involve more sophisticated logic
    # and potentially other dedicated content moderation APIs.
    response = client.analyze_entities(request={
        "document": document,
        "encoding_type": language_v1.EncodingType.UTF8
    })

    unsafe_indicators = [
        "violence", "hate speech", "sexual content", "profanity",
        "drugs", "weapons", "terrorism",
    ]
    
    found_unsafe_terms: List[str] = []
    for entity in response.entities:
        for indicator in unsafe_indicators:
            if indicator in entity.name.lower() or indicator in entity.type.name.lower():
                found_unsafe_terms.append(entity.name)
                break

    is_unsafe = len(found_unsafe_terms) > 0

    return {
        "translated_text": payload["translated_text"],
        "is_unsafe": is_unsafe,
        "found_terms": list(set(found_unsafe_terms)),
        "message": "Content deemed potentially unsafe." if is_unsafe else "Content appears safe."
    }
