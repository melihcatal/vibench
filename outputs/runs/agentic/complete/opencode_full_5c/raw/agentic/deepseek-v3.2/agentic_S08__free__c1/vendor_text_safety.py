import os
from typing import Dict, List, Any, Optional
from document_models import ExpenseRecord


def moderate_vendor_text(
    vendor_notes: str, vendor_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Moderate vendor notes or memo fields using Google Cloud Natural Language API.
    """
    from google.cloud import language_v2

    # Initialize Google Cloud Natural Language client
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError(
            "GOOGLE_APPLICATION_CREDENTIALS environment variable is required"
        )

    client = language_v2.LanguageServiceClient()

    # Prepare text for analysis
    text_to_analyze = vendor_notes
    if vendor_name:
        text_to_analyze = f"{vendor_name}: {vendor_notes}"

    # Analyze sentiment
    document = language_v2.Document(
        content=text_to_analyze,
        type_=language_v2.Document.Type.PLAIN_TEXT,
        language_code="en",
    )

    moderation_results = {
        "is_safe": True,
        "moderation_categories": {},
        "sentiment_score": 0.0,
        "sentiment_magnitude": 0.0,
        "provider": "google_cloud_natural_language",
        "moderation_timestamp": os.getenv("MODERATION_TIMESTAMP", ""),
    }

    try:
        # Analyze sentiment
        sentiment_response = client.analyze_sentiment(request={"document": document})

        sentiment = sentiment_response.document_sentiment
        moderation_results["sentiment_score"] = sentiment.score
        moderation_results["sentiment_magnitude"] = sentiment.magnitude

        # Moderate content for safety
        moderation_response = client.moderate_text(request={"document": document})

        # Check moderation categories
        for category in moderation_response.moderation_categories:
            moderation_results["moderation_categories"][category.name] = {
                "confidence": category.confidence,
                "threshold": category.threshold,
            }

            # Mark as unsafe if confidence exceeds threshold for harmful categories
            harmful_categories = [
                "Toxic",
                "Insult",
                "Profanity",
                "Derogatory",
                "Violent",
                "Sexually Explicit",
                "Harassment",
            ]

            if category.name in harmful_categories and category.confidence > 0.5:
                moderation_results["is_safe"] = False

        # Additional text analysis
        # Analyze entities
        entities_response = client.analyze_entities(request={"document": document})

        entities = []
        for entity in entities_response.entities:
            entity_info = {
                "name": entity.name,
                "type": language_v2.Entity.Type(entity.type_).name,
                "salience": entity.salience,
            }
            entities.append(entity_info)

        moderation_results["entities"] = entities

        # Analyze syntax
        syntax_response = client.analyze_syntax(request={"document": document})

        tokens = []
        for token in syntax_response.tokens:
            token_info = {
                "text": token.text.content,
                "part_of_speech": language_v2.PartOfSpeech.Tag(
                    token.part_of_speech.tag
                ).name,
                "dependency_edge": {
                    "head_token_index": token.dependency_edge.head_token_index,
                    "label": language_v2.DependencyEdge.Label(
                        token.dependency_edge.label
                    ).name,
                },
            }
            tokens.append(token_info)

        moderation_results["syntax_analysis"] = {
            "token_count": len(tokens),
            "language": syntax_response.language,
        }

        # Classify content
        classification_response = client.classify_text(request={"document": document})

        categories = []
        for category in classification_response.categories:
            categories.append(
                {"name": category.name, "confidence": category.confidence}
            )

        moderation_results["content_categories"] = categories

        # Calculate overall safety score
        safety_score = 1.0
        for category_name, category_data in moderation_results[
            "moderation_categories"
        ].items():
            if category_name in harmful_categories:
                # Reduce safety score based on harmful category confidence
                safety_score *= 1.0 - min(category_data["confidence"], 0.9)

        moderation_results["safety_score"] = safety_score

        # Add text statistics
        text_length = len(text_to_analyze)
        word_count = len(text_to_analyze.split())

        moderation_results["text_statistics"] = {
            "character_count": text_length,
            "word_count": word_count,
            "average_word_length": text_length / word_count if word_count > 0 else 0,
        }

    except Exception as e:
        moderation_results["error"] = str(e)
        moderation_results["is_safe"] = False  # Default to unsafe on error

    return moderation_results
