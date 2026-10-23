"""Check platform model output for unsafe content using Amazon Comprehend.

Uses the Amazon Comprehend DetectToxicContent API (boto3) to analyze
generated text for toxicity, hate speech, profanity, and other
potentially unsafe categories.
Auth: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
Provider: Amazon Comprehend Toxicity Detection
"""

from typing import Dict, List, Optional

from model_client import get_comprehend_client
from model_models import SafetyResult


def check_platform_output_safety(
    text: str,
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
) -> SafetyResult:
    """Check text for unsafe content using Amazon Comprehend DetectToxicContent.

    Sends the text to the Comprehend DetectToxicContent API and
    aggregates per-label confidence scores. Returns a SafetyResult
    with is_safe flag and individual category scores.
    """
    if not text or not text.strip():
        return SafetyResult(
            is_safe=True,
            scores={},
            raw_response={"message": "Empty text, considered safe"},
        )

    client = get_comprehend_client(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    response = client.detect_toxic_content(
        TextSegments=[{"Text": text}],
        LanguageCode="en",
    )

    result_list = response.get("ResultList", [])
    if not result_list:
        return SafetyResult(
            is_safe=True,
            scores={},
            raw_response=response,
        )

    segment = result_list[0]
    labels = segment.get("Labels", [])
    scores: Dict[str, float] = {}
    is_safe = True

    for label in labels:
        name = label.get("Name", "unknown")
        score = label.get("Score", 0.0)
        scores[name] = score
        # Amazon Comprehend toxicity threshold: scores above 0.5 are flagged
        if score > 0.5:
            is_safe = False

    return SafetyResult(
        is_safe=is_safe,
        scores=scores,
        raw_response=response,
    )


def check_multiple_segments(
    texts: List[str],
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
) -> List[SafetyResult]:
    """Check multiple text segments in a single Comprehend call."""
    if not texts:
        return []

    client = get_comprehend_client(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    segments = [{"Text": t} for t in texts if t and t.strip()]
    if not segments:
        return []

    response = client.detect_toxic_content(
        TextSegments=segments,
        LanguageCode="en",
    )

    results: List[SafetyResult] = []
    for segment in response.get("ResultList", []):
        labels = segment.get("Labels", [])
        scores: Dict[str, float] = {}
        is_safe = True
        for label in labels:
            name = label.get("Name", "unknown")
            score = label.get("Score", 0.0)
            scores[name] = score
            if score > 0.5:
                is_safe = False
        results.append(SafetyResult(is_safe=is_safe, scores=scores, raw_response=segment))

    return results


if __name__ == "__main__":
    sample = "This is a perfectly normal text about technology."
    result = check_platform_output_safety(sample)
    print(f"Safe: {result.is_safe}")
    print(f"Scores: {result.scores}")
