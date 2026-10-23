import os
import json
import boto3

from safety_models import ModerationScore, ModerationDecision, HarmCategory, ModerationResult

def get_aws_secrets_manager_client():
    region = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client("secretsmanager", region_name=region)

def get_thresholds(secret_name: str) -> dict:
    secrets_client = get_aws_secrets_manager_client()
    try:
        get_secret_value_response = secrets_client.get_secret_value(
            SecretId=secret_name
        )
        if 'SecretString' in get_secret_value_response:
            return json.loads(get_secret_value_response['SecretString'])
        else:
            raise ValueError("SecretString not found in AWS Secrets Manager response.")
    except Exception as e:
        print(f"Error fetching secret '{secret_name}': {e}")
        return {
            HarmCategory.TOXICITY.value: 0.8,
            HarmCategory.SEXUAL.value: 0.7,
            HarmCategory.VIOLENCE.value: 0.8,
            HarmCategory.HARASSMENT.value: 0.8,
            HarmCategory.HATE_SPEECH.value: 0.75,
            HarmCategory.DANGEROUS_CONTENT.value: 0.85,
        }

def apply_safety_thresholds(
    moderation_result: ModerationResult,
    secret_name: str = "safety-thresholds"
) -> ModerationDecision:
    
    thresholds = get_thresholds(secret_name)
    
    overall_decision = "ALLOW"
    violation_reasons = []

    for score_item in moderation_result.scores:
        category_threshold = thresholds.get(score_item.category.value, 1.0)
        if score_item.score >= category_threshold:
            overall_decision = "BLOCK"
            violation_reasons.append(f"{score_item.category.value} score ({score_item.score:.2f}) exceeds threshold ({category_threshold:.2f})")
    
    reason_str = ", ".join(violation_reasons) if violation_reasons else "No violations detected."

    return ModerationDecision(
        text=moderation_result.text,
        decision=overall_decision,
        reason=reason_str
    )