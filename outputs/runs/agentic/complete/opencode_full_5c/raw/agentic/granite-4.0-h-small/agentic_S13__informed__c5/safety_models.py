# safety_models.py

import os
from typing import List, Dict, Any
from ibm_watsonx_ai.hlp import HlpClient  # watsonx guardrails SDK
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

class SafetyResponseNormalizer:
    """Normalize watsonx guardrails moderation response into a common dict format."""
    @staticmethod
    def normalize(raw: Dict[str, Any]) -> Dict[str, Any]:
        # Example raw structure from HlpClient.analyze()
        # {
        #     "hate": 0.85,
        #     "abuse": 0.12,
        #     "profanity": 0.03,
        # }
        standardized = {cat: raw.get(cat, 0.0) for cat in ["hate", "abuse", "profanity"]}
        return standardized

    @staticmethod
def categorize(score: Dict[str, Any], thresholds: Dict[str, float]) -> List[str]:
        """Return list of categories that exceed their thresholds."""
        flagged = []
        for cat, thresh in thresholds.items():
            if score.get(cat, 0.0) >= thresh:
                flagged.append(cat)
        return flagged

# Example usage of the utilities (for local testing)
if __name__ == "__main__":
    client = get_safety_client()
    raw = client.analyze(text="I hate you and want to fight you.")
    norm = SafetyResponseNormalizer.normalize(raw)
    print("Normalized:", norm)
    thresholds = {"hate": 0.7, "abuse": 0.5}
    flagged = SafetyResponseNormalizer.categorize(norm, thresholds)
    print("Flagged categories:", flagged)
