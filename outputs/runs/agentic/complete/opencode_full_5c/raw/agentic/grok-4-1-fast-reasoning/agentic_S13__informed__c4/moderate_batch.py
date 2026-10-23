import boto3
from typing import List
from safety_models import SafetyResult


def moderate_batch(texts: List[str]) -> List[SafetyResult]:
    client = boto3.client("comprehend", region_name="us-east-1")
    text_segments = [{"Text": text} for text in texts[:25]]
    response = client.batch_detect_toxicity(
        TextSegments=text_segments, LanguageCode="en"
    )
    results: List[SafetyResult] = []
    for item in response.get("ResultList", []):
        res = item["Result"]
        score = res.get("Score", 0.0)
        results.append(
            {
                "categories": {"toxicity": score},
                "overall_blocked": score > 0.5,
                "rationale": f"Amazon Comprehend toxicity score: {score:.2f}",
                "redacted_text": "",
                "flagged_spans": [],
                "raw_response": res,
            }
        )
    for error in response.get("ErrorList", []):
        print(f"Error at index {error['Index']}: {error['Error']}")
    return results
