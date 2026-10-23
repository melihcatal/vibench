import os
import json
from boto3 import client as boto3_client
from safety_client import load_aws_ssm_client
from safety_models import ModerationResult

class ThresholdDecision:
    def __init__(self, allow: bool, reason: str):
        self.allow = allow
        self.reason = reason

def get_thresholds(ssm_client, parameter_name: str) -> dict:
    try:
        response = ssm_client.get_parameter(Name=parameter_name, WithDecryption=True)
        return json.loads(response['Parameter']['Value'])
    except ssm_client.exceptions.ParameterNotFound:
        # Default thresholds if not found in SSM
        return {
            "hate": 0.9,
            "self_harm": 0.9,
            "sexual": 0.9,
            "violence": 0.9,
            "general_flag_score": 0.95 # for a general 'is_flagged' score if available
        }

def apply_safety_threshold(moderation_result: ModerationResult, parameter_name: str) -> ThresholdDecision:
    ssm_client = load_aws_ssm_client()
    thresholds = get_thresholds(ssm_client, parameter_name)

    # Check overall flagged status first if available
    if moderation_result.is_flagged and 'general_flag_score' in thresholds:
        # Assuming 'is_flagged' implies a high score overall, though specific scores are preferred.
        # If specific scores are all below threshold but general flag is true, might need more nuance.
        pass # Let category checks override or refine

    for category, score in moderation_result.category_scores.items():
        if category in thresholds and score >= thresholds[category]:
            return ThresholdDecision(allow=False, reason=f"Text exceeded threshold for category '{category}' (score: {score:.2f} >= threshold: {thresholds[category]:.2f})")

    return ThresholdDecision(allow=True, reason="Text is within safety thresholds.")
