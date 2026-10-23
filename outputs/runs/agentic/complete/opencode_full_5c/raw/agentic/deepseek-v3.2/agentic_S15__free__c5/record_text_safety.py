import os
import json
from typing import Dict, Any, List
from google.cloud import language_v1


def record_text_safety(
    document: Dict[str, Any], fields_to_check: List[str] = None
) -> Dict[str, Any]:
    """
    Check user-generated document fields for unsafe content using Google Cloud Natural Language API.

    Args:
        document: Document to check
        fields_to_check: List of field names to check (defaults to all string fields)

    Returns:
        dict: Safety analysis results
    """
    client = language_v1.LanguageServiceClient.from_service_account_json(
        os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    )

    if fields_to_check is None:
        # Check all string fields
        fields_to_check = []
        for key, value in document.items():
            if isinstance(value, str) and len(value) > 0:
                fields_to_check.append(key)

    results = {
        "document_id": document.get("id", "unknown"),
        "fields_checked": [],
        "unsafe_fields": [],
        "safety_scores": {},
        "overall_safe": True,
    }

    for field in fields_to_check:
        if field not in document:
            continue

        field_value = document[field]
        if not isinstance(field_value, str) or not field_value.strip():
            continue

        try:
            # Analyze sentiment and entities for safety indicators
            document_obj = language_v1.Document(
                content=field_value,
                type_=language_v1.Document.Type.PLAIN_TEXT,
                language="en",
            )

            # Analyze sentiment
            sentiment_response = client.analyze_sentiment(
                request={"document": document_obj}
            )

            # Analyze entities
            entity_response = client.analyze_entities(
                request={"document": document_obj}
            )

            # Check for potentially unsafe content
            # Negative sentiment could indicate problematic content
            sentiment_score = sentiment_response.document_sentiment.score
            sentiment_magnitude = sentiment_response.document_sentiment.magnitude

            # Check for specific entity types that might indicate unsafe content
            unsafe_entity_types = ["PERSON", "LOCATION", "EVENT", "ORGANIZATION"]
            found_entities = []

            for entity in entity_response.entities:
                if entity.type_.name in unsafe_entity_types:
                    found_entities.append(
                        {
                            "name": entity.name,
                            "type": entity.type_.name,
                            "salience": entity.salience,
                        }
                    )

            field_result = {
                "field": field,
                "sentiment_score": sentiment_score,
                "sentiment_magnitude": sentiment_magnitude,
                "found_entities": found_entities,
                "text_length": len(field_value),
                "is_safe": True,
            }

            # Simple safety heuristic
            if sentiment_score < -0.5 or sentiment_magnitude > 2.0:
                field_result["is_safe"] = False
                results["unsafe_fields"].append(field)
                results["overall_safe"] = False

            results["fields_checked"].append(field)
            results["safety_scores"][field] = field_result

        except Exception as e:
            # Log error but continue with other fields
            error_result = {"field": field, "error": str(e), "is_safe": False}
            results["fields_checked"].append(field)
            results["unsafe_fields"].append(field)
            results["safety_scores"][field] = error_result
            results["overall_safe"] = False

    return results
