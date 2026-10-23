import os
import re
from typing import Optional, List, Dict, Any
import boto3
from botocore.config import Config

from detect_image_labels import detect_image_labels, ImageLabelResponse
from score_image_safety import score_image_safety, ImageSafetyResponse


AWS_REGION = os.environ.get(
    "AWS_DEFAULT_REGION", os.environ.get("AWS_REGION", "us-east-1")
)
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_COMPREHEND_ENDPOINT = os.environ.get("AWS_COMPREHEND_ENDPOINT", None)

_comprehend_client = None

UNSAFE_TEXT_PATTERNS = [
    r"(?:hate|racist|slur|discriminat)",
    r"(?:violence|kill|murder|attack)",
    r"(?:explicit|nsfw|porn|sexual)",
    r"(?:drug|cocaine|heroin|meth)",
    r"(?:weapon|gun|knife|bomb)",
]


def get_comprehend_client() -> boto3.client:
    global _comprehend_client

    if _comprehend_client is not None:
        return _comprehend_client

    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )

    config = Config(
        retries={"max_attempts": 3, "mode": "adaptive"},
        read_timeout=30,
        connect_timeout=30,
    )

    kwargs = {"config": config}
    if AWS_COMPREHEND_ENDPOINT:
        kwargs["endpoint_url"] = AWS_COMPREHEND_ENDPOINT

    _comprehend_client = session.client("comprehend", **kwargs)
    return _comprehend_client


def check_text_safety(text: str) -> Dict[str, Any]:
    client = get_comprehend_client()

    sentiment_response = client.detect_sentiment(
        Text=text,
        LanguageCode="en",
    )

    toxic_phrases = []
    for pattern in UNSAFE_TEXT_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            toxic_phrases.append(pattern)

    is_unsafe = (
        sentiment_response.get("Sentiment") == "NEGATIVE" or len(toxic_phrases) > 0
    )

    sentiment_score = sentiment_response.get("SentimentScore", {})

    return {
        "is_unsafe": is_unsafe,
        "sentiment": sentiment_response.get("Sentiment"),
        "sentiment_scores": sentiment_score,
        "toxic_patterns_found": toxic_phrases,
        "model": "aws-comprehend-detect-sentiment-v3",
    }


def visual_safety_text(
    image_path: Optional[str] = None,
    image_bytes: Optional[bytes] = None,
    check_labels: bool = True,
    check_safety_flags: bool = True,
) -> Dict[str, Any]:
    results = {
        "image_source": image_path or "<bytes>",
        "label_safety": None,
        "text_safety": None,
        "overall_safe": True,
        "flags": [],
        "model": "aws-comprehend-visual-safety-v3",
    }

    if check_labels:
        labels_result = detect_image_labels(
            image_path=image_path,
            image_bytes=image_bytes,
            max_labels=20,
        )

        label_text = " ".join(lbl.name.lower() for lbl in labels_result.labels)
        label_safety = check_text_safety(label_text)
        results["label_safety"] = label_safety

        if label_safety["is_unsafe"]:
            results["overall_safe"] = False
            results["flags"].extend(label_safety.get("toxic_patterns_found", []))

    if check_safety_flags:
        safety_result = score_image_safety(
            image_path=image_path,
            image_bytes=image_bytes,
        )

        if not safety_result.is_safe:
            results["overall_safe"] = False
            results["flags"].extend(
                [det.name for det in safety_result.unsafe_detections]
            )

    return results


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("Usage: python visual_safety_text.py <image_path>")
        sys.exit(1)

    result = visual_safety_text(image_path=sys.argv[1])
    print(json.dumps(result, indent=2))
