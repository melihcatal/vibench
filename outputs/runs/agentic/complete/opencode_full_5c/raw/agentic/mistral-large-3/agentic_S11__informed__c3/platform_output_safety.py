import os
import json
from typing import Dict, Any

import requests


def check_bedrock_guardrails(
    text: str, guardrail_identifier: str = "toxicity"
) -> Dict[str, Any]:
    """
    Check text for unsafe content using Amazon Comprehend Toxicity Analysis.
    """
    client = boto3.client(
        service_name="comprehend",
        region_name=os.getenv("AWS_REGION", "us-west-2"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    try:
        response = client.detect_toxic_content(
            TextSegments=[{"Text": text}], LanguageCode="en"
        )

        toxicity_scores = response["ResultList"][0]["Labels"]

        return {
            "is_toxic": any(label["Score"] > 0.7 for label in toxicity_scores),
            "toxicity_scores": {
                label["Name"]: label["Score"] for label in toxicity_scores
            },
            "provider": "aws_comprehend",
        }
    except Exception as e:
        raise Exception(f"Failed to check toxicity: {e}")
