# safety_models.py
import os
from typing import Dict, Any

def load_model_conf(model_name: str) -> Dict[str, Any]:
    """Placeholder for loading configuration specific to a moderation model.
    In a real project you could store config (e.g., required categories, default thresholds) per provider/model.
    For Azure we simply return a generic config."
    return {
        "provider": "azure",
        "model": model_name,
        "default_thresholds": {
            "hate": 0.6,
            "self_harm": 0.6,
            "sexual": 0.6,
            "violence": 0.6
        },
        "required_categories": ["hate", "self_harm", "sexual", "violence"]
    }

if __name__ == "__main__":
    # Example: load Azure Content Safety config
    conf = load_model_conf("azure_content_safety")
    print(conf)