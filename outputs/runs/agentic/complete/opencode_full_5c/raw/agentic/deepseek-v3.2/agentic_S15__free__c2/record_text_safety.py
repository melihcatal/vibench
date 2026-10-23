import os
from typing import Dict, Any, List
from google.cloud import language_v1


def check_text_safety(documents: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Check user-generated document fields for unsafe content using Google Cloud Natural Language API.

    Args:
        documents: List of document records to check

    Returns:
        dict: Safety check results
    """
    try:
        # Initialize Google Cloud Natural Language client
        client = language_v1.LanguageServiceClient()

        results = []
        unsafe_count = 0

        for doc in documents:
            doc_id = doc.get("id", "unknown")
            doc_data = doc.get("data", {})

            # Extract text content from document
            text_content = extract_text_from_document(doc_data)

            if not text_content:
                results.append(
                    {
                        "document_id": doc_id,
                        "safe": True,
                        "reason": "No text content to analyze",
                        "categories": [],
                    }
                )
                continue

            # Analyze sentiment and entities (which includes content classification)
            document = language_v1.Document(
                content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
            )

            # Analyze sentiment
            sentiment_response = client.analyze_sentiment(
                request={"document": document}
            )

            # Analyze entities
            entity_response = client.analyze_entities(request={"document": document})

            # Check for potentially unsafe content
            unsafe_categories = []

            # Check sentiment extremes (very negative might indicate harmful content)
            if sentiment_response.document_sentiment.score < -0.8:
                unsafe_categories.append("highly_negative_sentiment")

            # Check for specific entity types that might indicate unsafe content
            for entity in entity_response.entities:
                entity_type = language_v1.Entity.Type(entity.type_).name
                if entity_type in ["PERSON", "LOCATION", "EVENT"]:
                    # These might need context-specific checking
                    pass

            # Classify content (this would detect explicit content, hate speech, etc.)
            # Note: Content classification requires additional setup in Google Cloud
            # For this example, we'll use a simplified check

            is_safe = len(unsafe_categories) == 0

            if not is_safe:
                unsafe_count += 1

            results.append(
                {
                    "document_id": doc_id,
                    "safe": is_safe,
                    "categories": unsafe_categories,
                    "sentiment_score": sentiment_response.document_sentiment.score,
                    "sentiment_magnitude": sentiment_response.document_sentiment.magnitude,
                    "entity_count": len(entity_response.entities),
                }
            )

        return {
            "success": True,
            "results": results,
            "summary": {
                "total_documents": len(documents),
                "unsafe_documents": unsafe_count,
                "safe_documents": len(documents) - unsafe_count,
                "unsafe_percentage": (unsafe_count / len(documents) * 100)
                if documents
                else 0,
            },
            "service_used": "google-cloud-language-api",
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "service_used": "google-cloud-language-api",
        }


def extract_text_from_document(doc_data: Any) -> str:
    """
    Extract text content from document data for analysis.

    Args:
        doc_data: Document data (dict, string, or other)

    Returns:
        str: Extracted text content
    """
    if isinstance(doc_data, dict):
        # Extract string values from dictionary
        text_parts = []
        for key, value in doc_data.items():
            if isinstance(value, str):
                text_parts.append(value)
            elif isinstance(value, (int, float, bool)):
                text_parts.append(str(value))
            elif isinstance(value, dict):
                # Recursively extract from nested dicts
                nested_text = extract_text_from_document(value)
                if nested_text:
                    text_parts.append(nested_text)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        text_parts.append(item)
        return " ".join(text_parts)
    elif isinstance(doc_data, str):
        return doc_data
    elif doc_data is None:
        return ""
    else:
        return str(doc_data)


def check_single_document(document: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check safety of a single document.

    Args:
        document: Single document record

    Returns:
        dict: Safety check results
    """
    result = check_text_safety([document])
    if result["success"]:
        # Extract single result
        single_result = result["results"][0] if result["results"] else {}
        return {
            "success": True,
            "document_id": single_result.get("document_id"),
            "safe": single_result.get("safe", True),
            "categories": single_result.get("categories", []),
            "sentiment_score": single_result.get("sentiment_score"),
            "sentiment_magnitude": single_result.get("sentiment_magnitude"),
            "entity_count": single_result.get("entity_count"),
            "service_used": "google-cloud-language-api",
        }
    else:
        return result


def batch_safety_check(document_ids: List[str], fetch_function) -> Dict[str, Any]:
    """
    Perform batch safety check by fetching documents and checking them.

    Args:
        document_ids: List of document IDs to check
        fetch_function: Function to fetch documents by ID

    Returns:
        dict: Batch safety check results
    """
    documents = []

    for doc_id in document_ids:
        try:
            result = fetch_function(doc_id)
            if result.get("success") and result.get("data"):
                documents.append({"id": doc_id, "data": result["data"]})
        except Exception as e:
            # Skip documents that can't be fetched
            continue

    return check_text_safety(documents)
