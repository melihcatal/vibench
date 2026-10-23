from google.cloud import language_v1
from speech_client import get_nl_client
from speech_models import SafetyAssessment, SafetyRating
from typing import List


def check_safety(text: str) -> SafetyAssessment:
    client = get_nl_client()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Available features: SENTIMENT, ENTITY, SYNTAX, CLASSIFY_TEXT, MODERATION
    # MODERATION is what we need for safety checks
    response = client.moderate_text(document=document)

    ratings: List[SafetyRating] = []
    for category_filter in response.moderation_categories:
        ratings.append(
            SafetyRating(category=category_filter.name, score=category_filter.score)
        )

    return SafetyAssessment(ratings=ratings)
