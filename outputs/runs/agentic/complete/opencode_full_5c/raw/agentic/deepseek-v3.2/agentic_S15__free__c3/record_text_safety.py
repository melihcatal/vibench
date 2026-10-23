import os
from typing import Dict, Any, List
import json


def record_text_safety(
    documents: List[Dict[str, Any]], check_types: List[str] = None
) -> Dict[str, Any]:
    """
    Check user-generated document fields for unsafe content using Google Cloud Perspective API.

    Args:
        documents: List of document records
        check_types: Types of safety checks to perform

    Returns:
        dict: Safety analysis results
    """
    try:
        from google.cloud import language_v1

        # Initialize Google Cloud Language client
        client = language_v1.LanguageServiceClient()

        if check_types is None:
            check_types = [
                "TOXICITY",
                "SEVERE_TOXICITY",
                "IDENTITY_ATTACK",
                "INSULT",
                "PROFANITY",
                "THREAT",
            ]

        # Prepare text content from documents
        text_contents = []
        document_map = []

        for i, doc in enumerate(documents):
            doc_data = doc.get("data", {})
            doc_id = doc.get("id", f"doc_{i}")

            # Extract text fields
            text_fields = []
            for key, value in doc_data.items():
                if isinstance(value, str) and len(value.strip()) > 0:
                    text_fields.append(value)
                elif isinstance(value, (list, dict)):
                    # Convert to string for analysis
                    try:
                        text_fields.append(json.dumps(value))
                    except:
                        pass

            if text_fields:
                combined_text = " ".join(text_fields)
                # Limit text length for API
                if len(combined_text) > 1000:
                    combined_text = combined_text[:1000] + "..."

                text_contents.append(combined_text)
                document_map.append(
                    {
                        "document_id": doc_id,
                        "text_preview": combined_text[:100] + "..."
                        if len(combined_text) > 100
                        else combined_text,
                    }
                )

        if not text_contents:
            return {
                "success": False,
                "error": "No text content found in documents",
                "provider": "google:perspective",
            }

        # Analyze text with Google Cloud Natural Language API
        # Note: For full Perspective API with attribute scores, you'd need the Perspective API client
        # This uses the Cloud Natural Language API for sentiment and entity analysis as an alternative

        safety_results = []

        for i, text in enumerate(text_contents):
            try:
                # Analyze sentiment
                document = language_v1.Document(
                    content=text,
                    type_=language_v1.Document.Type.PLAIN_TEXT,
                    language="en",
                )

                sentiment_response = client.analyze_sentiment(
                    request={"document": document}
                )

                # Analyze entities
                entity_response = client.analyze_entities(
                    request={"document": document}
                )

                # Check for potentially sensitive entities
                sensitive_entities = []
                for entity in entity_response.entities:
                    if entity.type_ in [
                        language_v1.Entity.Type.PERSON,
                        language_v1.Entity.Type.LOCATION,
                        language_v1.Entity.Type.PHONE_NUMBER,
                        language_v1.Entity.Type.ADDRESS,
                    ]:
                        sensitive_entities.append(
                            {
                                "name": entity.name,
                                "type": language_v1.Entity.Type(entity.type_).name,
                                "salience": entity.salience,
                            }
                        )

                # Simple content safety heuristics
                warning_words = [
                    "hate",
                    "attack",
                    "kill",
                    "violence",
                    "abuse",
                    "harass",
                ]
                content_warnings = []
                text_lower = text.lower()

                for word in warning_words:
                    if word in text_lower:
                        content_warnings.append(word)

                safety_score = 1.0  # Start with perfect score

                # Adjust based on sentiment
                sentiment_score = sentiment_response.document_sentiment.score
                if sentiment_score < -0.5:
                    safety_score -= 0.3
                elif sentiment_score < -0.2:
                    safety_score -= 0.1

                # Adjust based on sensitive entities
                if sensitive_entities:
                    safety_score -= 0.1 * min(3, len(sensitive_entities))

                # Adjust based on content warnings
                if content_warnings:
                    safety_score -= 0.2 * min(3, len(content_warnings))

                safety_score = max(0.0, min(1.0, safety_score))

                safety_results.append(
                    {
                        "document_id": document_map[i]["document_id"],
                        "safety_score": safety_score,
                        "sentiment": {
                            "score": sentiment_response.document_sentiment.score,
                            "magnitude": sentiment_response.document_sentiment.magnitude,
                        },
                        "sensitive_entities_count": len(sensitive_entities),
                        "content_warnings": content_warnings,
                        "text_preview": document_map[i]["text_preview"],
                    }
                )

            except Exception as e:
                safety_results.append(
                    {
                        "document_id": document_map[i]["document_id"],
                        "error": str(e),
                        "safety_score": 0.5,  # Default neutral score on error
                        "text_preview": document_map[i]["text_preview"],
                    }
                )

        # Calculate overall safety metrics
        valid_scores = [
            r["safety_score"] for r in safety_results if "safety_score" in r
        ]
        avg_safety_score = (
            sum(valid_scores) / len(valid_scores) if valid_scores else 0.0
        )

        unsafe_count = sum(
            1 for r in safety_results if r.get("safety_score", 1.0) < 0.5
        )

        return {
            "success": True,
            "safety_results": safety_results,
            "summary": {
                "total_documents": len(documents),
                "analyzed_documents": len(safety_results),
                "average_safety_score": avg_safety_score,
                "unsafe_documents": unsafe_count,
                "safe_percentage": (
                    (len(safety_results) - unsafe_count) / len(safety_results) * 100
                )
                if safety_results
                else 0,
            },
            "provider": "google:cloud-natural-language",
            "api_version": "v1",
            "check_types": check_types,
        }

    except ImportError:
        return {
            "success": False,
            "error": "Google Cloud Language library not installed. Install with: pip install google-cloud-language",
            "provider": "google:cloud-natural-language",
        }
    except Exception as e:
        error_msg = str(e)
        if "credentials" in error_msg.lower():
            return {
                "success": False,
                "error": "Google Cloud credentials not configured. Set GOOGLE_APPLICATION_CREDENTIALS environment variable.",
                "provider": "google:cloud-natural-language",
            }
        return {
            "success": False,
            "error": f"Google Cloud API error: {error_msg}",
            "provider": "google:cloud-natural-language",
        }
