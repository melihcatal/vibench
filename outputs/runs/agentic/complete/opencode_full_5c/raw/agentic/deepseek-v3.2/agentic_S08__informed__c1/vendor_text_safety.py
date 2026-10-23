import os
import json
from typing import Dict, Any, List
import boto3
from botocore.exceptions import ClientError


def moderate_vendor_text(text: str) -> Dict[str, Any]:
    """
    Moderate vendor notes or memo fields using Amazon Comprehend.
    """
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        raise ValueError("AWS credentials not configured")

    comprehend = boto3.client(
        "comprehend",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )

    if not text or len(text.strip()) == 0:
        return {
            "is_safe": True,
            "moderation_categories": {},
            "overall_score": 0.0,
            "flagged": False,
            "error": "Empty text provided",
        }

    try:
        response = comprehend.detect_toxic_content(
            TextSegments=[{"Text": text}], LanguageCode="en"
        )

        results = response["ResultList"][0] if response["ResultList"] else {}

        moderation_categories = {}
        max_score = 0.0
        flagged = False

        if "Toxicity" in results:
            for toxicity in results["Toxicity"]:
                category = toxicity["Name"]
                score = toxicity["Score"]
                moderation_categories[category] = score

                if score > max_score:
                    max_score = score

                if score > 0.5:
                    flagged = True

        return {
            "is_safe": not flagged,
            "moderation_categories": moderation_categories,
            "overall_score": max_score,
            "flagged": flagged,
            "text_length": len(text),
            "language": "en",
        }

    except ClientError as e:
        return {
            "is_safe": False,
            "error": f"AWS Comprehend error: {str(e)}",
            "moderation_categories": {},
            "overall_score": 1.0,
            "flagged": True,
        }

    except Exception as e:
        return {
            "is_safe": False,
            "error": f"Unexpected error: {str(e)}",
            "moderation_categories": {},
            "overall_score": 1.0,
            "flagged": True,
        }


def check_vendor_notes_safety(
    vendor_notes: str, memo_field: str = ""
) -> Dict[str, Any]:
    """
    Check safety of vendor notes and memo fields.
    """
    all_text = vendor_notes
    if memo_field:
        all_text += f" {memo_field}"

    moderation_result = moderate_vendor_text(all_text)

    safety_report = {
        "vendor_notes": vendor_notes[:100] + "..."
        if len(vendor_notes) > 100
        else vendor_notes,
        "memo_field": memo_field[:100] + "..." if len(memo_field) > 100 else memo_field,
        "moderation_result": moderation_result,
        "recommendation": "APPROVE"
        if moderation_result.get("is_safe", False)
        else "REVIEW",
        "timestamp": __import__("datetime").datetime.now().isoformat(),
    }

    if moderation_result.get("flagged", False):
        toxic_categories = []
        for category, score in moderation_result.get(
            "moderation_categories", {}
        ).items():
            if score > 0.5:
                toxic_categories.append(f"{category}: {score:.2f}")

        safety_report["warning"] = (
            f"Content flagged in categories: {', '.join(toxic_categories)}"
        )

    return safety_report
