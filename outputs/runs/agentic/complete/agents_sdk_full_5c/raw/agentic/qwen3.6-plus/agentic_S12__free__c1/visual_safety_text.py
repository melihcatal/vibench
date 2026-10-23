"""
visual_safety_text.py - Check generated visual labels for unsafe text
using Amazon Comprehend for content analysis.

Provider: Amazon Comprehend (boto3 SDK)
API hostname: https://comprehend.{region}.amazonaws.com
"""

import os
from typing import List, Dict, Any, Optional

import boto3
from botocore.config import Config

from detect_image_labels import detect_labels, detect_labels_from_bytes
from detect_image_text import detect_text, extract_text_strings
from vision_models import LabelDetectionResponse, TextDetectionResponse

AWS_COMPREHEND_REGION = os.environ.get("AWS_REGION", "us-east-1")
AWS_COMPREHEND_SERVICE = "comprehend"


def get_comprehend_client() -> boto3.client:
    """Create and return a configured Amazon Comprehend client."""
    session = boto3.Session(
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=AWS_COMPREHEND_REGION,
    )
    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        connect_timeout=10,
        read_timeout=30,
    )
    return session.client("comprehend", config=config)


def check_label_text_safety(
    labels_response: LabelDetectionResponse,
) -> Dict[str, Any]:
    """
    Check generated visual labels for unsafe or policy-sensitive text content
    using Amazon Comprehend content moderation.

    Analyzes the combined text of detected image labels for offensive,
    sexually explicit, or otherwise unsafe language using Comprehend's
    DetectToxicContent API.

    Args:
        labels_response: Results from label detection.

    Returns:
        Dictionary with safety assessment results including toxicity scores.
    """
    client = get_comprehend_client()

    label_text = " ".join([l.name for l in labels_response.labels])

    if not label_text.strip():
        return {
            "is_safe": True,
            "toxicity_results": [],
            "overall_score": 0.0,
        }

    response = client.detect_toxic_content(
        TextSegments=[{"Text": label_text}],
        LanguageCode="en",
    )

    results = response.get("ResultList", [])
    overall_toxicity = 0.0
    toxic_items = []

    for result in results:
        for label in result.get("Labels", []):
            name = label.get("Name", "")
            score = label.get("Score", 0.0)
            if score > 0.5:
                toxic_items.append({"label": name, "score": score})
                overall_toxicity = max(overall_toxicity, score)

    is_safe = overall_toxicity < 0.5

    return {
        "is_safe": is_safe,
        "toxicity_results": toxic_items,
        "overall_score": overall_toxicity,
        "label_text_analyzed": label_text,
    }


def check_detected_text_safety(
    text_response: TextDetectionResponse,
) -> Dict[str, Any]:
    """
    Check OCR-detected text from images for unsafe content using Amazon Comprehend.

    Analyzes all text detected within an image (via Rekognition DetectText)
    for toxic, offensive, or policy-violating language using Comprehend's
    DetectToxicContent API.

    Args:
        text_response: Results from text detection.

    Returns:
        Dictionary with safety assessment of detected image text.
    """
    client = get_comprehend_client()

    text_segments = [
        {"Text": t.text}
        for t in text_response.detected_text
        if t.text.strip()
    ]

    if not text_segments:
        return {
            "is_safe": True,
            "toxicity_results": [],
            "overall_score": 0.0,
        }

    response = client.detect_toxic_content(
        TextSegments=text_segments,
        LanguageCode="en",
    )

    results = response.get("ResultList", [])
    overall_toxicity = 0.0
    toxic_items = []

    for result in results:
        for label in result.get("Labels", []):
            name = label.get("Name", "")
            score = label.get("Score", 0.0)
            if score > 0.5:
                toxic_items.append({"label": name, "score": score})
                overall_toxicity = max(overall_toxicity, score)

    is_safe = overall_toxicity < 0.5

    return {
        "is_safe": is_safe,
        "toxicity_results": toxic_items,
        "overall_score": overall_toxicity,
    }


def check_image_text_safety_full(
    image_path: str,
    min_confidence: float = 50.0,
) -> Dict[str, Any]:
    """
    Run a full safety check on both visual labels and detected text for an image.

    Combines Rekognition label detection, Rekognition text detection, and
    Comprehend toxic content analysis into a single safety assessment.

    Args:
        image_path: Path to the local image file.
        min_confidence: Confidence threshold for vision APIs.

    Returns:
        Combined safety assessment dictionary.
    """
    labels_response = detect_labels(image_path, min_confidence=min_confidence)
    text_response = detect_text(image_path, min_confidence=min_confidence)

    label_safety = check_label_text_safety(labels_response)
    text_safety = check_detected_text_safety(text_response)

    combined_is_safe = label_safety["is_safe"] and text_safety["is_safe"]
    combined_score = max(
        label_safety["overall_score"], text_safety["overall_score"]
    )

    return {
        "is_safe": combined_is_safe,
        "overall_score": combined_score,
        "label_safety": label_safety,
        "text_safety": text_safety,
    }


def print_visual_safety_results(results: Dict[str, Any]) -> None:
    """Print visual text safety analysis results."""
    status = "SAFE" if results["is_safe"] else "UNSAFE TEXT DETECTED"
    print(f"Visual Text Safety: {status} (toxicity score: {results['overall_score']:.2f})")

    if results["label_safety"]["toxicity_results"]:
        print("\nUnsafe label content:")
        for item in results["label_safety"]["toxicity_results"]:
            print(f"  - {item['label']}: {item['score']:.2f}")

    if results["text_safety"]["toxicity_results"]:
        print("\nUnsafe detected text:")
        for item in results["text_safety"]["toxicity_results"]:
            print(f"  - {item['label']}: {item['score']:.2f}")
