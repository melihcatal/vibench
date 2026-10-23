from google.cloud import language_v1
from typing import Dict, Any


def document_field_extraction(text: str) -> Dict[str, Any]:
    client = language_v1.LanguageServiceClient()
    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = client.analyze_entities(request={"document": document})
    fields = {}
    for entity in response.entities:
        fields[entity.name] = {
            "type": entity.type_,
            "salience": entity.salience,
            "mentions": [m.type_.name for m in entity.mentions],
        }
    return {"fields": fields}
