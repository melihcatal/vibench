import os
import json
from typing import Dict, Any, List
import boto3
from botocore.exceptions import ClientError


def check_platform_output_safety(
    text: str, language_code: str = "en"
) -> Dict[str, Any]:
    """Check platform model output for unsafe content using Amazon Comprehend."""

    # Initialize AWS Comprehend client with Bedrock guardrails integration
    comprehend_client = boto3.client(
        "comprehend",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    try:
        # Use Amazon Comprehend DetectToxicContent API
        response = comprehend_client.detect_toxic_content(
            TextSegments=[{"Text": text}], LanguageCode=language_code
        )

        # Process results
        results = []
        for result in response["ResultList"]:
            toxicity_scores = {}
            for label in result["Labels"]:
                toxicity_scores[label["Name"]] = label["Score"]

            results.append(
                {
                    "text_segment": result["TextSegment"]["Text"],
                    "toxicity_scores": toxicity_scores,
                    "overall_toxicity": max(toxicity_scores.values())
                    if toxicity_scores
                    else 0.0,
                }
            )

        # Determine if content is safe
        is_safe = True
        unsafe_reasons = []

        for result in results:
            overall_toxicity = result["overall_toxicity"]
            if overall_toxicity > 0.5:  # Threshold for toxicity
                is_safe = False
                unsafe_reasons.append(
                    {
                        "text": result["text_segment"],
                        "toxicity_score": overall_toxicity,
                        "threshold_exceeded": True,
                    }
                )

            # Check specific toxicity categories
            for category, score in result["toxicity_scores"].items():
                if score > 0.7:  # Higher threshold for severe categories
                    is_safe = False
                    unsafe_reasons.append(
                        {"category": category, "score": score, "threshold": 0.7}
                    )

        return {
            "provider": "amazon-comprehend",
            "service": "DetectToxicContent",
            "is_safe": is_safe,
            "results": results,
            "unsafe_reasons": unsafe_reasons if not is_safe else [],
            "language_code": language_code,
            "text_length": len(text),
        }

    except ClientError as e:
        # Fallback to basic content check if Comprehend fails
        print(f"Amazon Comprehend error: {e}")

        # Basic keyword-based safety check as fallback
        unsafe_keywords = ["hate", "violence", "harassment", "self-harm", "sexual"]
        found_keywords = []

        for keyword in unsafe_keywords:
            if keyword.lower() in text.lower():
                found_keywords.append(keyword)

        is_safe = len(found_keywords) == 0

        return {
            "provider": "fallback-basic",
            "service": "keyword-check",
            "is_safe": is_safe,
            "unsafe_keywords": found_keywords,
            "warning": "Amazon Comprehend service unavailable, using basic keyword check",
        }
