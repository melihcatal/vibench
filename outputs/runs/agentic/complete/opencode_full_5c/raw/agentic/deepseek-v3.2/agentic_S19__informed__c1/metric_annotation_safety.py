import os
import json
from typing import Dict, Any, List, Optional
import boto3
from botocore.exceptions import ClientError


def check_annotation_safety(text: str, language_code: str = "en") -> Dict[str, Any]:
    """
    Check free-text metric labels or annotations for unsafe text using Amazon Comprehend.

    Args:
        text: The text to check for safety
        language_code: Language code (default: "en")

    Returns:
        Safety analysis results
    """
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    if not access_key or not secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
        )

    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
    )

    comprehend = session.client("comprehend")

    try:
        response = comprehend.detect_toxic_content(
            TextSegments=[{"Text": text}], LanguageCode=language_code
        )

        results = []
        for result in response["ResultList"]:
            toxicity_scores = {}
            for score in result["Labels"]:
                toxicity_scores[score["Name"].lower()] = score["Score"]

            results.append(
                {
                    "text_segment": result.get("Text", text),
                    "toxicity_scores": toxicity_scores,
                    "max_toxicity_score": max(toxicity_scores.values())
                    if toxicity_scores
                    else 0.0,
                }
            )

        max_overall_score = (
            max([r["max_toxicity_score"] for r in results]) if results else 0.0
        )

        safety_assessment = {
            "is_safe": max_overall_score < 0.5,
            "max_toxicity_score": max_overall_score,
            "high_risk_categories": [],
            "recommendation": "safe" if max_overall_score < 0.5 else "review_needed",
        }

        if results:
            first_result = results[0]
            for category, score in first_result["toxicity_scores"].items():
                if score >= 0.7:
                    safety_assessment["high_risk_categories"].append(
                        {"category": category, "score": score, "severity": "high"}
                    )
                elif score >= 0.5:
                    safety_assessment["high_risk_categories"].append(
                        {"category": category, "score": score, "severity": "medium"}
                    )

        return {
            "text_analyzed": text,
            "language_code": language_code,
            "results": results,
            "safety_assessment": safety_assessment,
            "service_used": "Amazon Comprehend Toxic Content Detection",
        }

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "UnsupportedLanguageException":
            return {
                "text_analyzed": text,
                "language_code": language_code,
                "error": f"Language {language_code} not supported by Amazon Comprehend",
                "service_used": "Amazon Comprehend Toxic Content Detection",
            }
        else:
            raise


def check_multiple_annotations(
    annotations: List[str], language_code: str = "en"
) -> Dict[str, Any]:
    """
    Check multiple annotations for safety.

    Args:
        annotations: List of text annotations to check
        language_code: Language code

    Returns:
        Combined safety analysis
    """
    results = []
    unsafe_count = 0
    high_risk_count = 0

    for annotation in annotations:
        if not annotation.strip():
            continue

        result = check_annotation_safety(annotation, language_code)
        results.append(result)

        if not result.get("safety_assessment", {}).get("is_safe", True):
            unsafe_count += 1

        high_risk_cats = result.get("safety_assessment", {}).get(
            "high_risk_categories", []
        )
        for cat in high_risk_cats:
            if cat.get("severity") == "high":
                high_risk_count += 1
                break

    overall_safe = unsafe_count == 0

    return {
        "total_annotations": len(annotations),
        "checked_annotations": len(results),
        "unsafe_annotations": unsafe_count,
        "high_risk_annotations": high_risk_count,
        "overall_safe": overall_safe,
        "detailed_results": results,
        "recommendation": "all_safe" if overall_safe else "review_needed",
    }


def validate_metric_labels(labels: Dict[str, str]) -> Dict[str, Any]:
    """
    Validate metric labels for safety.

    Args:
        labels: Dictionary of metric labels

    Returns:
        Validation results
    """
    text_to_check = []
    label_context = {}

    for key, value in labels.items():
        if value and isinstance(value, str):
            text_to_check.append(f"{key}: {value}")
            label_context[value] = key

    if not text_to_check:
        return {
            "labels_checked": 0,
            "all_safe": True,
            "details": "No text content to check",
        }

    combined_text = " ".join(text_to_check)
    safety_result = check_annotation_safety(combined_text)

    unsafe_labels = []
    if not safety_result.get("safety_assessment", {}).get("is_safe", True):
        for text in text_to_check:
            individual_check = check_annotation_safety(text.split(": ", 1)[1])
            if not individual_check.get("safety_assessment", {}).get("is_safe", True):
                label_key = text.split(": ", 1)[0]
                unsafe_labels.append(
                    {
                        "label": label_key,
                        "value": text.split(": ", 1)[1],
                        "safety_result": individual_check,
                    }
                )

    return {
        "labels_checked": len(text_to_check),
        "all_safe": len(unsafe_labels) == 0,
        "combined_safety_result": safety_result,
        "unsafe_labels": unsafe_labels,
        "recommendation": "safe"
        if len(unsafe_labels) == 0
        else f"review {len(unsafe_labels)} label(s)",
    }


if __name__ == "__main__":
    test_annotation = "CPU utilization is critically high on production server"

    result = check_annotation_safety(test_annotation)
    print(f"Safety check result: {json.dumps(result, indent=2, default=str)}")

    test_labels = {
        "environment": "production",
        "severity": "critical",
        "note": "Server needs immediate attention",
    }

    label_result = validate_metric_labels(test_labels)
    print(f"\nLabel validation: {label_result['all_safe']}")
