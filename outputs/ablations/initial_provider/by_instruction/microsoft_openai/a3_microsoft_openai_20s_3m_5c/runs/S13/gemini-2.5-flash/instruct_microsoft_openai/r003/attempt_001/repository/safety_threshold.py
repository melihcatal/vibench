from typing import Dict
from safety_client import get_aws_ssm_client
from safety_models import ModerationResponse

def get_thresholds_from_ssm() -> Dict[str, float]:
    client = get_aws_ssm_client()
    # Assume thresholds are stored as a JSON string in a single SSM parameter
    # e.g., /content-safety/thresholds = '{"hate": 0.5, "sexual": 0.7}'
    try:
        response = client.get_parameter(Name='/content-safety/thresholds', WithDecryption=True)
        import json
        return json.loads(response['Parameter']['Value'])
    except client.exceptions.ParameterNotFound:
        print("SSM parameter /content-safety/thresholds not found. Using default thresholds.")
        return {
            "hate": 0.5,
            "sexual": 0.5,
            "violence": 0.5,
            "self_harm": 0.5,
        }
    except Exception as e:
        print(f"Error fetching thresholds from SSM: {e}. Using default thresholds.")
        return {
            "hate": 0.5,
            "sexual": 0.5,
            "violence": 0.5,
            "self_harm": 0.5,
        }

def apply_safety_thresholds(moderation_response: ModerationResponse) -> bool:
    thresholds = get_thresholds_from_ssm()

    for category, score in moderation_response.category_scores.items():
        if category in thresholds and score > thresholds[category]:
            return False  # Text is not allowed if any category exceeds its threshold
    return True  # Text is allowed if all categories are within thresholds
