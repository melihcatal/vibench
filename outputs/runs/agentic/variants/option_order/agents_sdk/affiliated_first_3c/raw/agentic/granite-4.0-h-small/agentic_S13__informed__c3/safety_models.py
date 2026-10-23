import os

class SafetyModels:
    """Helper definitions for request/response normalization across providers."""
    # Mapping from provider-specific category names to generic ones
    CATEGORY_MAP = {
        'hate': 'hate',
        'hate_speech': 'hate',
        'self_harm': 'self_harm',
        'self-injury': 'self_harm',
        'sexual': 'sexual',
        'sexual_content': 'sexual',
        'violence': 'violence',
        'graphic_violence': 'violence',
        # add more mappings as needed
    }

    @staticmethod
    def normalize_categories(raw_categories: dict) -> dict:
        """Convert provider-specific category names to generic ones."""
        normalized = {}
        for raw_cat, score in raw_categories.items():
            generic_cat = SafetyModels.CATEGORY_MAP.get(raw_cat.lower(), raw_cat.lower())
            normalized[generic_cat] = score
        return normalized

    @staticmethod
    def safe_score(categories: dict, thresholds: dict) -> bool:
        """Determine if text is safe based on normalized categories and thresholds."""
        for cat, score in categories.items():
            if cat in thresholds and score > thresholds[cat]:
                return False
        return True