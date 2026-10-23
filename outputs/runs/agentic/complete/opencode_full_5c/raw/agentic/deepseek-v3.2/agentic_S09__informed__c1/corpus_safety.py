import os
import json
from typing import List, Dict, Any
import boto3
from botocore.exceptions import ClientError


def corpus_safety(texts: List[str]) -> Dict[str, Any]:
    """Check corpus text before embedding using Amazon Comprehend Toxicity Detection."""
    client = boto3.client(
        "comprehend",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    results = {
        "total_texts": len(texts),
        "safe_texts": 0,
        "unsafe_texts": 0,
        "flagged_details": [],
        "overall_safe": True,
    }

    for i, text in enumerate(texts):
        try:
            # Truncate text if too long for Comprehend
            truncated_text = text[:5000] if len(text) > 5000 else text

            response = client.detect_toxic_content(
                TextSegments=[{"Text": truncated_text}], LanguageCode="en"
            )

            # Check if any toxicity score exceeds threshold
            toxic_scores = response["ResultList"][0]["Labels"]
            max_toxicity = (
                max(score["Score"] for score in toxic_scores) if toxic_scores else 0
            )
            threshold = 0.5

            if max_toxicity > threshold:
                results["unsafe_texts"] += 1
                results["flagged_details"].append(
                    {
                        "text_index": i,
                        "text_preview": text[:100] + "..." if len(text) > 100 else text,
                        "max_toxicity_score": max_toxicity,
                        "toxic_labels": [
                            {"Name": label["Name"], "Score": label["Score"]}
                            for label in toxic_scores
                            if label["Score"] > threshold
                        ],
                    }
                )
            else:
                results["safe_texts"] += 1

        except ClientError as e:
            # If API fails for a text, mark as unsafe to be cautious
            results["unsafe_texts"] += 1
            results["flagged_details"].append(
                {
                    "text_index": i,
                    "text_preview": text[:100] + "..." if len(text) > 100 else text,
                    "error": str(e),
                }
            )

    results["overall_safe"] = results["unsafe_texts"] == 0

    return results
