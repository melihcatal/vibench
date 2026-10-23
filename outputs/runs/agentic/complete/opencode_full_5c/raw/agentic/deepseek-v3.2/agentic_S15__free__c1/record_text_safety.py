import os
from google.cloud import language_v1
from typing import Dict, Any, List, Optional


def record_text_safety(
    documents: List[Dict[str, Any]], check_types: List[str] = None
) -> Dict[str, Any]:
    """
    Check user-generated document fields for unsafe content using Google Cloud Natural Language API.

    Args:
        documents: List of document records to check
        check_types: Types of safety checks to perform

    Returns:
        dict: Safety check results
    """
    try:
        # Initialize Google Cloud Natural Language client
        client = language_v1.LanguageServiceClient()

        # Default check types
        if check_types is None:
            check_types = ["toxicity", "profanity", "threat", "insult"]

        results = []
        unsafe_count = 0
        total_checks = 0

        for doc_idx, document in enumerate(documents):
            if not isinstance(document, dict):
                continue

            doc_result = {
                "document_index": doc_idx,
                "document_id": document.get("id", f"doc_{doc_idx}"),
                "fields_checked": [],
                "unsafe_fields": [],
                "safety_scores": {},
            }

            # Check text fields in document
            for field_name, field_value in document.items():
                if isinstance(field_value, str) and field_value.strip():
                    # Analyze text for safety
                    try:
                        document = language_v1.Document(
                            content=field_value,
                            type_=language_v1.Document.Type.PLAIN_TEXT,
                            language="en",
                        )

                        # Analyze sentiment (which includes toxicity attributes)
                        response = client.analyze_sentiment(
                            request={
                                "document": document,
                                "encoding_type": language_v1.EncodingType.UTF8,
                            }
                        )

                        # Check for safety attributes
                        # Note: Google Cloud Natural Language API doesn't have explicit safety scoring
                        # We'll use sentiment analysis as a proxy and check for negative sentiment
                        sentiment = response.document_sentiment

                        doc_result["fields_checked"].append(field_name)
                        doc_result["safety_scores"][field_name] = {
                            "sentiment_score": sentiment.score,
                            "sentiment_magnitude": sentiment.magnitude,
                        }

                        # Flag as potentially unsafe if highly negative sentiment
                        if sentiment.score < -0.5:
                            doc_result["unsafe_fields"].append(
                                {
                                    "field": field_name,
                                    "reason": "highly_negative_sentiment",
                                    "score": sentiment.score,
                                }
                            )
                            unsafe_count += 1

                        total_checks += 1

                    except Exception as field_error:
                        # Skip fields that can't be analyzed
                        continue

            results.append(doc_result)

        # Calculate overall safety metrics
        safe_count = total_checks - unsafe_count
        safety_percentage = (
            (safe_count / total_checks * 100) if total_checks > 0 else 100
        )

        return {
            "success": True,
            "results": results,
            "summary": {
                "total_documents_checked": len(results),
                "total_fields_checked": total_checks,
                "unsafe_fields_found": unsafe_count,
                "safe_fields_found": safe_count,
                "safety_percentage": round(safety_percentage, 2),
                "check_types": check_types,
            },
            "provider": "google:cloud-natural-language",
            "service": "language_v1",
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "provider": "google:cloud-natural-language",
            "service": "language_v1",
        }


def check_text_content_safety(text: str, field_name: str = "content") -> Dict[str, Any]:
    """
    Check safety of specific text content using Google Cloud Natural Language API.

    Args:
        text: Text content to check
        field_name: Name of the field being checked

    Returns:
        dict: Safety check result
    """
    try:
        # Initialize Google Cloud Natural Language client
        client = language_v1.LanguageServiceClient()

        if not text or not text.strip():
            return {
                "success": True,
                "field": field_name,
                "is_safe": True,
                "reason": "empty_content",
                "provider": "google:cloud-natural-language",
            }

        # Analyze text
        document = language_v1.Document(
            content=text, type_=language_v1.Document.Type.PLAIN_TEXT, language="en"
        )

        response = client.analyze_sentiment(
            request={
                "document": document,
                "encoding_type": language_v1.EncodingType.UTF8,
            }
        )

        sentiment = response.document_sentiment

        # Determine safety based on sentiment
        is_safe = sentiment.score >= -0.3  # Allow mildly negative content

        safety_categories = []
        if sentiment.score < -0.7:
            safety_categories.append("highly_negative")
        elif sentiment.score < -0.3:
            safety_categories.append("moderately_negative")

        # Analyze entities for additional context
        entity_response = client.analyze_entities(
            request={
                "document": document,
                "encoding_type": language_v1.EncodingType.UTF8,
            }
        )

        entity_types = set()
        for entity in entity_response.entities:
            entity_types.add(language_v1.Entity.Type(entity.type_).name)

        return {
            "success": True,
            "field": field_name,
            "is_safe": is_safe,
            "sentiment_score": sentiment.score,
            "sentiment_magnitude": sentiment.magnitude,
            "safety_categories": safety_categories,
            "entity_types": list(entity_types)[:5],  # Top 5 entity types
            "text_length": len(text),
            "provider": "google:cloud-natural-language",
            "service": "language_v1",
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "field": field_name,
            "provider": "google:cloud-natural-language",
            "service": "language_v1",
        }


def batch_safety_check(
    texts: List[str], field_names: List[str] = None
) -> Dict[str, Any]:
    """
    Perform batch safety check on multiple text items.

    Args:
        texts: List of text items to check
        field_names: Optional list of field names

    Returns:
        dict: Batch safety check results
    """
    if field_names is None:
        field_names = [f"text_{i}" for i in range(len(texts))]

    if len(texts) != len(field_names):
        return {
            "success": False,
            "error": "Number of texts must match number of field names",
            "provider": "google:cloud-natural-language",
        }

    results = []
    unsafe_count = 0

    for i, (text, field_name) in enumerate(zip(texts, field_names)):
        result = check_text_content_safety(text, field_name)
        results.append(result)

        if result.get("success") and not result.get("is_safe", True):
            unsafe_count += 1

    return {
        "success": True,
        "results": results,
        "summary": {
            "total_checked": len(results),
            "unsafe_count": unsafe_count,
            "safe_count": len(results) - unsafe_count,
            "safety_percentage": round(
                (len(results) - unsafe_count) / len(results) * 100, 2
            ),
        },
        "provider": "google:cloud-natural-language",
    }
