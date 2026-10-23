"""
Check extracted document text for unsafe content using Amazon Comprehend.

Provider: Amazon Comprehend
Model/Feature: Amazon Comprehend DetectToxicContent API
"""

import os
from typing import List, Optional

import boto3
from botocore.config import Config

from document_models import SafetyRequest, SafetyResponse


# Provider-identifying: Amazon Comprehend endpoint
COMPREHEND_ENDPOINT = os.environ.get(
    "AWS_COMPREHEND_ENDPOINT", "https://comprehend.us-east-1.amazonaws.com"
)
COMPREHEND_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

# Amazon Comprehend language code for safety analysis
COMPREHEND_LANGUAGE_CODE = "en"

# Comprehend toxic content labels
TOXIC_LABELS = {
    "HATE": "Hate speech",
    "SEXUALLY_EXPLICIT": "Sexually explicit content",
    "DANGEROUS": "Dangerous or illegal content",
    "HARASSMENT": "Harassment or bullying",
    "SELF_HARM": "Self-harm content",
    "VIOLENCE": "Violent content",
    "DRUGS": "Drug-related content",
    "PROFANITY": "Profanity",
}


def create_comprehend_client(
    region_name: Optional[str] = None,
    max_retries: int = 3,
    timeout: int = 30,
) -> boto3.client:
    """
    Create a boto3 Comprehend client.

    Args:
        region_name: AWS region
        max_retries: Maximum retry attempts
        timeout: Request timeout in seconds

    Returns:
        Configured boto3 Comprehend client
    """
    config = Config(
        retries={"max_attempts": max_retries},
        connect_timeout=timeout,
        read_timeout=timeout,
    )

    session_kwargs = {"region_name": region_name or COMPREHEND_REGION}
    if AWS_ACCESS_KEY and AWS_SECRET_KEY:
        session_kwargs["aws_access_key_id"] = AWS_ACCESS_KEY
        session_kwargs["aws_secret_access_key"] = AWS_SECRET_KEY

    return boto3.client("comprehend", config=config, **session_kwargs)


def check_text_safety(text: str, toxicity_threshold: float = 0.7) -> SafetyResponse:
    """
    Check extracted document text for unsafe content using Amazon Comprehend.

    Uses the Amazon Comprehend DetectToxicContent API to analyze text
    for various categories of harmful content.

    Args:
        text: Extracted OCR text to analyze
        toxicity_threshold: Score threshold above which content is flagged

    Returns:
        SafetyResponse with safety assessment and category scores
    """
    client = create_comprehend_client()

    # Amazon Comprehend has a 5KB limit per text segment
    text_segments = _split_text_for_comprehend(text, max_length=5000)

    category_scores = {}
    max_toxicity = 0.0

    for segment in text_segments:
        if not segment.strip():
            continue

        response = client.detect_toxic_content(
            TextSegments=[{"Text": segment}],
            LanguageCode=COMPREHEND_LANGUAGE_CODE,
        )

        results = response.get("ResultList", [])
        for result in results:
            toxic_labels = result.get("Labels", [])
            for label in toxic_labels:
                label_name = label.get("Name", "")
                label_score = label.get("Score", 0.0)

                # Track maximum score per category
                if label_name not in category_scores:
                    category_scores[label_name] = 0.0
                category_scores[label_name] = max(
                    category_scores[label_name], label_score
                )
                max_toxicity = max(max_toxicity, label_score)

    is_safe = max_toxicity < toxicity_threshold

    # Map to human-readable category names
    readable_categories = {}
    for label_name, score in category_scores.items():
        readable_name = TOXIC_LABELS.get(label_name, label_name)
        readable_categories[readable_name] = score

    return SafetyResponse(
        is_safe=is_safe,
        categories=readable_categories,
        overall_confidence=1.0 - max_toxicity if is_safe else max_toxicity,
    )


def check_safety_with_categories(
    text: str,
    categories: Optional[List[str]] = None,
    toxicity_threshold: float = 0.7,
) -> SafetyResponse:
    """
    Check text safety with focus on specific categories.

    Args:
        text: Extracted OCR text to analyze
        categories: List of category names to focus on (e.g., ["HATE", "VIOLENCE"])
        toxicity_threshold: Score threshold for flagging

    Returns:
        SafetyResponse with category-specific results
    """
    response = check_text_safety(text, toxicity_threshold)

    if categories:
        # Filter to only requested categories
        filtered = {}
        for cat_name, score in response.categories.items():
            for requested in categories:
                if requested.upper() in cat_name.upper() or cat_name.upper() in requested.upper():
                    filtered[cat_name] = score
        response.categories = filtered
        response.is_safe = all(s < toxicity_threshold for s in filtered.values())

    return response


def batch_safety_check(texts: List[str], toxicity_threshold: float = 0.7) -> List[SafetyResponse]:
    """
    Check safety for multiple text segments.

    Args:
        texts: List of text strings to analyze
        toxicity_threshold: Score threshold for flagging

    Returns:
        List of SafetyResponse objects
    """
    return [check_text_safety(text, toxicity_threshold) for text in texts]


def get_safety_report(text: str, toxicity_threshold: float = 0.7) -> str:
    """
    Generate a human-readable safety report.

    Args:
        text: Extracted OCR text to analyze
        toxicity_threshold: Score threshold for flagging

    Returns:
        Formatted safety report string
    """
    response = check_text_safety(text, toxicity_threshold)

    report_lines = [
        f"Safety Analysis Report",
        f"Overall Safe: {'Yes' if response.is_safe else 'NO'}",
        f"Confidence: {response.overall_confidence:.1%}",
        "",
    ]

    if response.categories:
        report_lines.append("Category Scores:")
        for category, score in sorted(response.categories.items()):
            status = "FLAGGED" if score >= toxicity_threshold else "OK"
            report_lines.append(f"  [{status}] {category}: {score:.1%}")
    else:
        report_lines.append("No toxic content detected.")

    return "\n".join(report_lines)


def _split_text_for_comprehend(text: str, max_length: int = 5000) -> List[str]:
    """
    Split text into segments suitable for Comprehend API limits.

    Args:
        text: Text to split
        max_length: Maximum characters per segment

    Returns:
        List of text segments
    """
    segments = []
    if len(text) <= max_length:
        segments.append(text)
        return segments

    # Split on paragraph boundaries
    paragraphs = text.split("\n\n")
    current = ""

    for para in paragraphs:
        if len(current) + len(para) + 2 > max_length:
            if current:
                segments.append(current.strip())
                current = para
            else:
                # Single paragraph too long; split on sentences
                sentences = para.replace("\n", " ").split(". ")
                for sent in sentences:
                    if len(current) + len(sent) > max_length:
                        if current:
                            segments.append(current.strip())
                            current = ""
                    current += ". " + sent if current else sent
        else:
            current += "\n\n" + para if current else para

    if current.strip():
        segments.append(current.strip())

    return segments


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python ocr_safety.py <text_file>")
        sys.exit(1)

    text_file = sys.argv[1]
    with open(text_file, "r", encoding="utf-8") as f:
        text = f.read()

    report = get_safety_report(text)
    print(report)
