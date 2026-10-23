from typing import Dict, List, Any
from google.cloud import language_v1


def record_text_safety(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    client = language_v1.LanguageServiceClient()

    safety_results = []
    for document in documents:
        text_content = " ".join(
            str(value) for value in document.get("document_data", {}).values()
        )

        response = client.moderate_text(
            request={
                "document": {
                    "type_": language_v1.Document.Type.PLAIN_TEXT,
                    "content": text_content,
                }
            }
        )

        safety_results.append(
            {
                "document_id": document.get("id"),
                "safety_attributes": {
                    "toxicity": response.moderation_result.toxicity,
                    "sexual_explicit": response.moderation_result.sexual_explicit,
                    "violent": response.moderation_result.violent,
                    "obscene": response.moderation_result.obscene,
                    "derogatory": response.moderation_result.derogatory,
                    "toxic": response.moderation_result.toxic,
                },
            }
        )

    return safety_results
