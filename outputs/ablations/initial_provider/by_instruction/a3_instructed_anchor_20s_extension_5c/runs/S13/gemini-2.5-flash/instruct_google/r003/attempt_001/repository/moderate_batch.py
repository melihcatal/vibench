from typing import List
from safety_client import SafetyClient
from safety_models import ModerationResult, SafetyRating

def moderate_batch(texts: List[str]) -> List[ModerationResult]:
    """
    Moderates a batch of user messages and returns per-message decisions using Google Vertex AI.
    """
    safety_client = SafetyClient()
    batch_results = []

    for text in texts:
        moderation_response = safety_client.moderate_text_with_vertex_ai(text)
        safety_ratings_data = moderation_response.get("safety_ratings", [])

        safety_ratings = []
        is_allowed = True
        reasons = []

        for rating_data in safety_ratings_data:
            safety_rating = SafetyRating(
                category=rating_data["category"],
                probability=rating_data["probability"],
                blocked=rating_data["blocked"]
            )
            safety_ratings.append(safety_rating)
            if safety_rating.blocked:
                is_allowed = False
                reasons.append(f"Blocked due to {safety_rating.category} with probability {safety_rating.probability}")

        batch_results.append(ModerationResult(
            text=text,
            safety_ratings=safety_ratings,
            is_allowed=is_allowed,
            reasons=reasons
        ))

    return batch_results
