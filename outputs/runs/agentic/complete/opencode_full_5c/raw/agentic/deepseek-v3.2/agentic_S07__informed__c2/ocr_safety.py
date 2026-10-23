import os
from typing import Dict, Any, List
import boto3
from botocore.config import Config


def check_text_safety(text: str) -> Dict[str, Any]:
    """
    Check extracted document text for unsafe content using Amazon Comprehend.

    Args:
        text: Text to check for safety

    Returns:
        Safety analysis results
    """
    # Initialize Amazon Comprehend client
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region_name = os.getenv("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError(
            "AWS credentials not found. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
        )

    comprehend_client = boto3.client(
        "comprehend",
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        config=Config(retries={"max_attempts": 3}),
    )

    # Detect toxic content
    try:
        toxicity_response = comprehend_client.detect_toxic_content(
            TextSegments=[{"Text": text}], LanguageCode="en"
        )

        # Process toxicity results
        toxic_scores = {}
        for result in toxicity_response.get("ResultList", []):
            for label in result.get("Labels", []):
                toxic_scores[label["Name"]] = label["Score"]

        # Detect PII (Personally Identifiable Information)
        pii_response = comprehend_client.detect_pii_entities(
            Text=text, LanguageCode="en"
        )

        pii_entities = []
        for entity in pii_response.get("Entities", []):
            pii_entities.append(
                {
                    "type": entity["Type"],
                    "score": entity["Score"],
                    "begin_offset": entity["BeginOffset"],
                    "end_offset": entity["EndOffset"],
                }
            )

        # Overall safety assessment
        max_toxicity = max(toxic_scores.values()) if toxic_scores else 0.0
        is_unsafe = max_toxicity > 0.5 or len(pii_entities) > 0

        return {
            "is_safe": not is_unsafe,
            "toxicity_scores": toxic_scores,
            "pii_entities": pii_entities,
            "max_toxicity_score": max_toxicity,
            "has_pii": len(pii_entities) > 0,
            "provider": "Amazon Comprehend",
        }

    except Exception as e:
        return {"is_safe": False, "error": str(e), "provider": "Amazon Comprehend"}


def analyze_document_safety(document_texts: List[str]) -> Dict[str, Any]:
    """
    Analyze safety of multiple document text segments.

    Args:
        document_texts: List of text segments from document

    Returns:
        Comprehensive safety analysis
    """
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region_name = os.getenv("AWS_REGION", "us-east-1")

    comprehend_client = boto3.client(
        "comprehend",
        region_name=region_name,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    all_results = []
    unsafe_segments = []

    for i, text in enumerate(document_texts):
        if len(text) > 5000:  # Comprehend limit
            text = text[:5000]

        try:
            # Detect toxic content for this segment
            toxicity_response = comprehend_client.detect_toxic_content(
                TextSegments=[{"Text": text}], LanguageCode="en"
            )

            segment_toxicity = {}
            for result in toxicity_response.get("ResultList", []):
                for label in result.get("Labels", []):
                    segment_toxicity[label["Name"]] = label["Score"]

            # Detect PII
            pii_response = comprehend_client.detect_pii_entities(
                Text=text, LanguageCode="en"
            )

            pii_entities = []
            for entity in pii_response.get("Entities", []):
                pii_entities.append({"type": entity["Type"], "score": entity["Score"]})

            max_toxicity = max(segment_toxicity.values()) if segment_toxicity else 0.0
            is_segment_unsafe = max_toxicity > 0.5 or len(pii_entities) > 0

            segment_result = {
                "segment_index": i,
                "text_preview": text[:100] + "..." if len(text) > 100 else text,
                "toxicity_scores": segment_toxicity,
                "pii_entities": pii_entities,
                "max_toxicity": max_toxicity,
                "is_unsafe": is_segment_unsafe,
            }

            all_results.append(segment_result)

            if is_segment_unsafe:
                unsafe_segments.append(i)

        except Exception as e:
            all_results.append(
                {
                    "segment_index": i,
                    "error": str(e),
                    "is_unsafe": True,  # Treat errors as unsafe
                }
            )
            unsafe_segments.append(i)

    # Overall assessment
    total_segments = len(document_texts)
    unsafe_count = len(unsafe_segments)

    return {
        "segment_analysis": all_results,
        "summary": {
            "total_segments": total_segments,
            "unsafe_segments": unsafe_count,
            "safe_segments": total_segments - unsafe_count,
            "unsafe_percentage": (unsafe_count / total_segments * 100)
            if total_segments > 0
            else 0,
            "overall_safe": unsafe_count == 0,
        },
        "unsafe_segment_indices": unsafe_segments,
        "provider": "Amazon Comprehend",
    }
