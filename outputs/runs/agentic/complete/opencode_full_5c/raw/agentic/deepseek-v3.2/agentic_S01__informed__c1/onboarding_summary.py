import os
import boto3
from botocore.config import Config
from typing import Dict, Any


def summarize_onboarding_state(user_data: Dict[str, Any]) -> str:
    """Summarize onboarding state for support using Amazon Bedrock with Titan model."""
    region = os.environ.get("AWS_REGION", "us-east-1")

    config = Config(region_name=region, retries={"max_attempts": 3, "mode": "standard"})

    bedrock_client = boto3.client("bedrock-runtime", config=config)

    prompt = f"""
    Summarize this user's onboarding state for support team review:
    
    User ID: {user_data.get("user_id", "N/A")}
    Email: {user_data.get("email", "N/A")}
    Registration Date: {user_data.get("registration_date", "N/A")}
    Onboarding Step: {user_data.get("onboarding_step", "N/A")}
    Profile Completion: {user_data.get("profile_completion", 0)}%
    Issues Encountered: {user_data.get("issues", [])}
    Last Activity: {user_data.get("last_activity", "N/A")}
    
    Provide a concise summary highlighting:
    1. Current onboarding status
    2. Any blockers or issues
    3. Recommended next steps for support
    """

    try:
        response = bedrock_client.invoke_model(
            modelId="amazon.titan-text-express-v1",
            contentType="application/json",
            accept="application/json",
            body=json.dumps(
                {
                    "inputText": prompt,
                    "textGenerationConfig": {
                        "maxTokenCount": 512,
                        "temperature": 0.3,
                        "topP": 0.9,
                    },
                }
            ),
        )

        response_body = json.loads(response["body"].read())
        summary = response_body["results"][0]["outputText"]

        return summary.strip()
    except Exception as e:
        print(f"Summary generation failed: {e}")
        return f"Onboarding summary unavailable. User: {user_data.get('email', 'Unknown')}, Step: {user_data.get('onboarding_step', 'Unknown')}"


def generate_support_notes(
    user_data: Dict[str, Any], support_context: str = ""
) -> Dict[str, Any]:
    """Generate structured support notes using Amazon Bedrock."""
    region = os.environ.get("AWS_REGION", "us-east-1")

    config = Config(region_name=region, retries={"max_attempts": 3, "mode": "standard"})

    bedrock_client = boto3.client("bedrock-runtime", config=config)

    prompt = f"""
    Generate structured support notes for this user onboarding case:
    
    User Context: {support_context}
    User Data: {json.dumps(user_data, indent=2)}
    
    Provide a JSON response with:
    1. priority_level (high/medium/low)
    2. issue_category (technical/profile/verification/other)
    3. recommended_action
    4. estimated_resolution_time (in hours)
    5. key_notes (bullet points)
    """

    try:
        response = bedrock_client.invoke_model(
            modelId="amazon.titan-text-express-v1",
            contentType="application/json",
            accept="application/json",
            body=json.dumps(
                {
                    "inputText": prompt,
                    "textGenerationConfig": {
                        "maxTokenCount": 1024,
                        "temperature": 0.2,
                        "topP": 0.8,
                    },
                }
            ),
        )

        response_body = json.loads(response["body"].read())
        notes_text = response_body["results"][0]["outputText"]

        import json as json_module

        try:
            notes_data = json_module.loads(notes_text)
        except:
            notes_data = {"raw_notes": notes_text}

        return notes_data
    except Exception as e:
        print(f"Support notes generation failed: {e}")
        return {
            "priority_level": "medium",
            "issue_category": "other",
            "recommended_action": "Manual review required",
            "estimated_resolution_time": 24,
            "key_notes": ["AI summary generation failed"],
        }


import json
