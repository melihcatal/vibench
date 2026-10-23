from typing import List, Dict, Any, Optional

class SafetyRating:
    def __init__(self, category: str, probability: str, blocked: bool):
        self.category = category
        self.probability = probability
        self.blocked = blocked

    def to_dict(self) -> Dict[str, Any]:
        return {
            "category": self.category,
            "probability": self.probability,
            "blocked": self.blocked
        }

class ModerationResponse:
    def __init__(self, text_content: str, provider: str, moderation_result: Dict[str, Any], error: Optional[str] = None):
        self.text_content = text_content
        self.provider = provider
        self.moderation_result = moderation_result
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        response = {
            "text_content": self.text_content,
            "provider": self.provider,
            "moderation_result": self.moderation_result
        }
        if self.error:
            response["error"] = self.error
        return response

class BatchModerationRequest:
    def __init__(self, texts: List[str], project_id: str, location: str = "us-central1"):
        self.texts = texts
        self.project_id = project_id
        self.location = location

class BatchModerationResponse:
    def __init__(self, results: List[ModerationResponse]):
        self.results = results

    def to_dict(self) -> Dict[str, Any]:
        return {"results": [res.to_dict() for res in self.results]}

def normalize_gemini_safety_ratings(candidates: List[Any]) -> List[SafetyRating]:
    normalized_ratings = []
    if candidates:
        for candidate in candidates:
            if hasattr(candidate, 'safety_ratings'):
                for rating in candidate.safety_ratings:
                    normalized_ratings.append(
                        SafetyRating(
                            category=rating.category.name,
                            probability=rating.probability.name,
                            blocked=rating.blocked
                        )
                    )
    return normalized_ratings

