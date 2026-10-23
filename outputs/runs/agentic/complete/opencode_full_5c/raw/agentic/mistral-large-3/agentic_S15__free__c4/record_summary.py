from typing import Dict, List, Any
import json
from google.cloud import language_v1


def record_summary(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    client = language_v1.LanguageServiceClient()

    summarized_documents = []
    for document in documents:
        text_content = json.dumps(document.get("document_data", {}))

        response = client.analyze_entities(
            request={
                "document": {
                    "type_": language_v1.Document.Type.PLAIN_TEXT,
                    "content": text_content,
                },
                "encoding_type": language_v1.EncodingType.UTF8,
            }
        )

        entities = [
            {"name": entity.name, "type": language_v1.Entity.Type(entity.type_).name}
            for entity in response.entities
        ]
        summarized_documents.append(
            {"document_id": document.get("id"), "summary": {"key_entities": entities}}
        )

    return summarized_documents
