"""Check free-text metric labels or annotations for unsafe text.

Uses Amazon Comprehend (boto3 SDK) to analyze metric labels, dashboard
annotations, and free-text fields for toxic or unsafe content.
Provider signals:
  - boto3.client("comprehend")
  - comprehend.detect_toxic_content API call
  - AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY environment variables
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import List, Optional

import boto3


@dataclass
class ToxicityLabelResult:
    """Result for a single label checked by Amazon Comprehend."""

    text: str
    is_toxic: bool
    labels: List[dict] = field(default_factory=list)
    toxicity_score: float = 0.0


def check_annotation_safety(
    texts: List[str],
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    aws_region: str = "us-east-1",
) -> List[ToxicityLabelResult]:
    """Check free-text metric labels or annotations for unsafe content
    using Amazon Comprehend.

    Parameters
    ----------
    texts : list[str]
        List of label/annotation strings to analyze.
    aws_access_key_id : str, optional
        AWS access key; falls back to environment variable AWS_ACCESS_KEY_ID.
    aws_secret_access_key : str, optional
        AWS secret key; falls back to environment variable AWS_SECRET_ACCESS_KEY.
    aws_region : str
        AWS region for the Comprehend endpoint.

    Returns
    -------
    list[ToxicityLabelResult]
        Safety analysis results for each text.
    """
    access_key = aws_access_key_id or os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = aws_secret_access_key or os.environ.get("AWS_SECRET_ACCESS_KEY")

    if not access_key or not secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are required for "
            "Amazon Comprehend toxicity detection."
        )

    comprehend = boto3.client(
        "comprehend",
        region_name=aws_region,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )

    results: List[ToxicityLabelResult] = []
    for text in texts:
        result = _check_single_text(comprehend, text)
        results.append(result)

    return results


def _check_single_text(
    comprehend,
    text: str,
) -> ToxicityLabelResult:
    """Run Amazon Comprehend detect_toxic_content on a single text string."""
    try:
        response = comprehend.detect_toxic_content(
            TextSegments=[{"Text": text}],
            LanguageCode="en",
        )
    except Exception:
        return ToxicityLabelResult(
            text=text,
            is_toxic=False,
            labels=[],
            toxicity_score=0.0,
        )

    labels = []
    max_toxicity = 0.0
    for segment_result in response.get("ResultList", []):
        for label in segment_result.get("Labels", []):
            name = label.get("Name", "")
            score = label.get("Score", 0.0)
            labels.append({"name": name, "score": score})
            if score > max_toxicity:
                max_toxicity = score

    # Consider toxic if any label exceeds 0.5 confidence
    is_toxic = max_toxicity > 0.5

    return ToxicityLabelResult(
        text=text,
        is_toxic=is_toxic,
        labels=labels,
        toxicity_score=max_toxicity,
    )


def filter_unsafe_annotations(
    annotations: List[dict],
    text_field: str = "label",
    **kwargs,
) -> List[dict]:
    """Filter out annotations containing unsafe text in the specified field.

    Parameters
    ----------
    annotations : list[dict]
        List of annotation dicts (e.g. metric dashboard labels).
    text_field : str
        Key within each annotation dict containing the text to check.
    **kwargs
        Passed through to check_annotation_safety.

    Returns
    -------
    list[dict]
        Annotations that passed safety checks.
    """
    texts = [ann.get(text_field, "") for ann in annotations]
    safety_results = check_annotation_safety(texts, **kwargs)

    safe_annotations = []
    for ann, safety in zip(annotations, safety_results):
        if not safety.is_toxic:
            safe_annotations.append(ann)

    return safe_annotations


if __name__ == "__main__":
    sample_texts = [
        "High CPU usage on production server",
        "This is a safe dashboard label",
    ]
    results = check_annotation_safety(sample_texts)
    for r in results:
        print(f"Text: {r.text!r} -> toxic={r.is_toxic} score={r.toxicity_score:.4f}")
