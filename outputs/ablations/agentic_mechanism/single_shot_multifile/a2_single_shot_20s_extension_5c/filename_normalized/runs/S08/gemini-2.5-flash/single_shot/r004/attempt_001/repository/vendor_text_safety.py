import os
from azure.cognitiveservices.vision.contentmoderator import ContentModeratorClient
from msrest.authentication import CognitiveServicesCredentials
from document_client import get_azure_content_moderator_client
from typing import Dict, Any

def moderate_vendor_text_azure(text: str, language: str = "eng") -> Dict[str, Any]:
    """
    Moderates vendor notes or memo fields using Azure Content Moderator.
    Returns a dictionary of moderation results.
    Requires AZURE_CONTENT_MODERATOR_ENDPOINT and AZURE_CONTENT_MODERATOR_KEY environment variables.
    """
    client = get_azure_content_moderator_client()

    screen_result = client.text_moderation.screen_text(
        text_content=text,
        language=language,
        classify=True,
        list_id=None,
        autocorrect=False,
        PII=False
    )

    moderation_summary = {
        "original_text": text,
        "is_profane": False,
        "profanity_terms": [],
        "classification_summary": None,
        "review_recommended": False
    }

    if screen_result.terms:
        moderation_summary["is_profane"] = True
        moderation_summary["profanity_terms"] = [
            {"term": term.term, "offset": term.offset} for term in screen_result.terms
        ]
        moderation_summary["review_recommended"] = True

    if screen_result.classification:
        classification = screen_result.classification
        moderation_summary["classification_summary"] = {
            "category1": {"score": classification.category1.score, "review_recommended": classification.category1.review_recommended},
            "category2": {"score": classification.category2.score, "review_recommended": classification.category2.review_recommended},
            "category3": {"score": classification.category3.score, "review_recommended": classification.category3.review_recommended},
            "is_review_recommended": classification.review_recommended
        }
        if classification.review_recommended:
            moderation_summary["review_recommended"] = True

    return moderation_summary
