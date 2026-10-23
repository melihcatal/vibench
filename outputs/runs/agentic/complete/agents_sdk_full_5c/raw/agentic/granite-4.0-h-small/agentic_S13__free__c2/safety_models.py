import json

class SafetyModels:
    """Local helpers for request payloads, response structures, and normalization."""
    MODERATION_MODEL_ID = "openai/moderations"

    @staticmethod
    def build_moderation_request(text: str) -> dict:
        """Prepare a request payload for the safety provider."""
        return {
            "input": text,
            "model": SafetyModels.MODERATION_MODEL_ID
        }

    @staticmethod
    def parse_moderation_response(raw: dict) -> dict:
        """Normalize provider response to a simple dict of categories and scores."""
        results = {}
        for category, details in raw['results'].items():
            results[category] = {
                "flagged": details['flagged'],
                "score": details['flag_details'][category]['score']
            }
        return results

    @staticmethod
    def normalize_response(raw: dict) -> dict:
        """Convenient wrapper to return a flat dict of bool flags per category."""
        parsed = SafetyModels.parse_moderation_response(raw)
        return {cat: data['flagged'] for cat, data in parsed.items()}
