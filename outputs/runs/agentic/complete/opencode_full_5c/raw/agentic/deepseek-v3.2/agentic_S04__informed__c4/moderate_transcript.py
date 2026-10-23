import os
import json
from typing import List, Dict, Any
import boto3
from botocore.exceptions import ClientError


def moderate_transcript_text(text: str) -> Dict[str, Any]:
    comprehend_client = boto3.client(
        "comprehend",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    try:
        response = comprehend_client.detect_toxic_content(
            TextSegments=[{"Text": text}], LanguageCode="en"
        )

        results = response.get("ResultList", [])
        if not results:
            return {
                "text": text,
                "is_toxic": False,
                "toxicity_scores": {},
                "flagged_categories": [],
            }

        result = results[0]
        labels = result.get("Labels", [])

        toxicity_scores = {}
        flagged_categories = []

        for label in labels:
            category = label["Name"]
            score = label["Score"]
            toxicity_scores[category] = score

            if score > 0.5:
                flagged_categories.append(category)

        return {
            "text": text,
            "is_toxic": len(flagged_categories) > 0,
            "toxicity_scores": toxicity_scores,
            "flagged_categories": flagged_categories,
            "highest_score": max(toxicity_scores.values()) if toxicity_scores else 0.0,
        }

    except ClientError as e:
        raise RuntimeError(f"Failed to moderate text: {e}")


def moderate_transcript_segments(
    segments: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    comprehend_client = boto3.client(
        "comprehend",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    moderated_segments = []

    for segment in segments:
        text = segment.get("text", "")
        if not text.strip():
            moderated_segments.append(
                {
                    **segment,
                    "moderation_result": {
                        "is_toxic": False,
                        "toxicity_scores": {},
                        "flagged_categories": [],
                    },
                }
            )
            continue

        try:
            response = comprehend_client.detect_toxic_content(
                TextSegments=[{"Text": text}], LanguageCode="en"
            )

            results = response.get("ResultList", [])
            if not results:
                moderation_result = {
                    "is_toxic": False,
                    "toxicity_scores": {},
                    "flagged_categories": [],
                }
            else:
                result = results[0]
                labels = result.get("Labels", [])

                toxicity_scores = {}
                flagged_categories = []

                for label in labels:
                    category = label["Name"]
                    score = label["Score"]
                    toxicity_scores[category] = score

                    if score > 0.5:
                        flagged_categories.append(category)

                moderation_result = {
                    "is_toxic": len(flagged_categories) > 0,
                    "toxicity_scores": toxicity_scores,
                    "flagged_categories": flagged_categories,
                    "highest_score": max(toxicity_scores.values())
                    if toxicity_scores
                    else 0.0,
                }

            moderated_segments.append(
                {**segment, "moderation_result": moderation_result}
            )

        except ClientError as e:
            print(f"Error moderating segment: {e}")
            moderated_segments.append(
                {
                    **segment,
                    "moderation_result": {
                        "is_toxic": False,
                        "toxicity_scores": {},
                        "flagged_categories": [],
                        "error": str(e),
                    },
                }
            )

    return moderated_segments


def check_content_safety(text: str) -> Dict[str, Any]:
    comprehend_client = boto3.client(
        "comprehend",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    try:
        toxic_response = comprehend_client.detect_toxic_content(
            TextSegments=[{"Text": text}], LanguageCode="en"
        )

        entities_response = comprehend_client.detect_entities(
            Text=text, LanguageCode="en"
        )

        toxic_results = toxic_response.get("ResultList", [])
        toxic_result = toxic_results[0] if toxic_results else {}

        toxicity_scores = {}
        flagged_categories = []

        for label in toxic_result.get("Labels", []):
            category = label["Name"]
            score = label["Score"]
            toxicity_scores[category] = score

            if score > 0.5:
                flagged_categories.append(category)

        entities = entities_response.get("Entities", [])
        sensitive_entities = [
            e for e in entities if e["Type"] in ["PERSON", "LOCATION", "ORGANIZATION"]
        ]

        return {
            "text": text,
            "is_toxic": len(flagged_categories) > 0,
            "toxicity_scores": toxicity_scores,
            "flagged_categories": flagged_categories,
            "entities_found": len(entities),
            "sensitive_entities": len(sensitive_entities),
            "safety_status": "SAFE" if len(flagged_categories) == 0 else "FLAGGED",
        }

    except ClientError as e:
        raise RuntimeError(f"Failed to check content safety: {e}")
