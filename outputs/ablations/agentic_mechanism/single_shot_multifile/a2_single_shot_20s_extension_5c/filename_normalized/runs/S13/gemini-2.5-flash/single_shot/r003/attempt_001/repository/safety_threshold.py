import os
from typing import Dict, Any
import boto3

from safety_client import get_aws_ssm_client
from safety_models import TextAnalysisResult, ModerationDecision

def get_moderation_thresholds(category: str) -> float:
    client = get_aws_ssm_client()
    parameter_name = f"/moderation/thresholds/{category.lower()}"
    try:
        response = client.get_parameter(
            Name=parameter_name,
            WithDecryption=True # Use WithDecryption if parameters are SecureString
        )
        return float(response['Parameter']['Value'])
    except client.exceptions.ParameterNotFound:
        print(f"Warning: Threshold for category '{category}' not found. Using default 0.8.")
        return 0.8 # Default threshold if not found
    except Exception as e:
        print(f"Error fetching threshold for {category}: {e}. Using default 0.8.")
        return 0.8

def apply_safety_threshold(analysis_result: TextAnalysisResult) -> ModerationDecision:
    is_allowed = True
    reasons_for_flagging = []

    for category, score in analysis_result.categories.items():
        threshold = get_moderation_thresholds(category)
        if score >= threshold:
            is_allowed = False
            reasons_for_flagging.append(f"{category} score ({score:.2f}) meets or exceeds threshold ({threshold:.2f})")
    
    decision_status = "Allowed" if is_allowed else "Flagged"

    return ModerationDecision(
        original_text=analysis_result.text,
        decision=decision_status,
        reasons=reasons_for_flagging,
        scores=analysis_result.categories
    )
