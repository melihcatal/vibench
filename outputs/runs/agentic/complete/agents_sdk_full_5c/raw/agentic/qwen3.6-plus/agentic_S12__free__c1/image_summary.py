"""
image_summary.py - Summarize visual analysis results by combining label detection,
image description, text detection, and safety scoring.

Provider: AWS Bedrock (Claude via boto3) for text summarization of combined vision results.
SDK: boto3 bedrock-runtime
"""

import os
import json
from typing import Dict, Any, Optional

import boto3
from botocore.config import Config

from vision_client import (
    get_rekognition_client,
    load_image_as_bytes,
    prepare_rekognition_image_payload,
    validate_image_size,
)
from vision_models import (
    LabelDetectionResponse,
    ImageDescriptionResponse,
    TextDetectionResponse,
    ImageSafetyResponse,
    normalize_rekognition_labels,
    normalize_rekognition_text,
    normalize_rekognition_moderation,
)
from detect_image_labels import detect_labels_from_bytes
from describe_image import describe_image_from_bytes
from detect_image_text import detect_text_from_bytes
from score_image_safety import score_image_safety_from_bytes

AWS_BEDROCK_MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")


def get_bedrock_runtime_client() -> boto3.client:
    """Create and return a configured AWS Bedrock Runtime client."""
    session = boto3.Session(
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=AWS_REGION,
    )
    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        connect_timeout=10,
        read_timeout=60,
    )
    return session.client("bedrock-runtime", config=config)


def build_analysis_context(
    labels_response: LabelDetectionResponse,
    description_response: ImageDescriptionResponse,
    text_response: TextDetectionResponse,
    safety_response: ImageSafetyResponse,
) -> Dict[str, Any]:
    """Build a structured context dict from all analysis results."""
    return {
        "labels": [
            {"name": l.name, "confidence": l.confidence}
            for l in labels_response.labels
        ],
        "description": description_response.description,
        "detected_text": [
            {"text": t.text, "confidence": t.confidence}
            for t in text_response.detected_text
        ],
        "safety": {
            "is_safe": safety_response.is_safe,
            "findings": [
                {"category": f.category, "confidence": f.confidence}
                for f in safety_response.findings
            ],
        },
    }


def summarize_visual_analysis(
    labels_response: LabelDetectionResponse,
    description_response: ImageDescriptionResponse,
    text_response: TextDetectionResponse,
    safety_response: ImageSafetyResponse,
    max_summary_length: int = 300,
) -> str:
    """
    Generate a concise summary of combined visual analysis results using AWS Bedrock Claude.

    Combines label detection, description, OCR text, and safety findings into
    a single summary via the Claude 3 Haiku model on AWS Bedrock.

    Args:
        labels_response: Results from label detection.
        description_response: Results from image description.
        text_response: Results from text detection.
        safety_response: Results from safety scoring.
        max_summary_length: Target maximum summary length.

    Returns:
        A concise textual summary of all visual analysis results.
    """
    context = build_analysis_context(
        labels_response, description_response, text_response, safety_response
    )
    context_json = json.dumps(context, indent=2)

    prompt = (
        f"You are a visual analysis summarizer. Given the following structured "
        f"analysis of an image, produce a concise summary of no more than {max_summary_length} characters. "
        f"Cover the main objects/scenes detected, any text found, the overall description, "
        f"and the safety status. Do not include JSON or markdown formatting.\n\n"
        f"Analysis context:\n{context_json}\n\n"
        f"Summary:"
    )

    client = get_bedrock_runtime_client()

    bedrock_payload = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 512,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "temperature": 0.3,
    }

    response = client.invoke_model(
        modelId=AWS_BEDROCK_MODEL_ID,
        body=json.dumps(bedrock_payload),
        contentType="application/json",
        accept="application/json",
    )

    response_body = json.loads(response["body"].read())
    summary = response_body.get("content", [{}])[0].get("text", "")

    if len(summary) > max_summary_length:
        summary = summary[:max_summary_length - 3] + "..."

    return summary


def run_full_analysis_and_summarize(
    image_path: str,
    min_confidence: float = 50.0,
) -> str:
    """
    Run all visual analyses on an image and produce a summary.

    Args:
        image_path: Path to the local image file.
        min_confidence: Confidence threshold for all analyses.

    Returns:
        Summary string of all visual analysis results.
    """
    image_bytes = load_image_as_bytes(image_path)

    labels_response = detect_labels_from_bytes(image_bytes, min_confidence=min_confidence)
    description_response = describe_image_from_bytes(image_bytes, min_confidence=min_confidence)
    text_response = detect_text_from_bytes(image_bytes, min_confidence=min_confidence)
    safety_response = score_image_safety_from_bytes(image_bytes, min_confidence=min_confidence)

    return summarize_visual_analysis(
        labels_response, description_response, text_response, safety_response
    )
