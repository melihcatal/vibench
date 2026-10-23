import os
import boto3
from botocore.exceptions import ClientError
from security_models import PayloadSafetyRequest, PayloadSafetyResponse
from security_client import get_comprehend_client


def check_payload_safety(text, categories=None):
    request = PayloadSafetyRequest(
        text=text,
        categories=categories,
    )
    client = get_comprehend_client()
    try:
        detect_response = client.detect_toxic_content(
            TextSegments=[{"Text": request.text}],
        )
        flags = []
        confidence_scores = {}
        is_safe = True
        for result in detect_response.get("ResultList", []):
            for label in result.get("Labels", []):
                label_name = label.get("Name", "")
                score = label.get("Score", 0.0)
                confidence_scores[label_name] = score
                if score > 0.5:
                    is_safe = False
                    flags.append(
                        {
                            "category": label_name,
                            "confidence": score,
                            "severity": "high" if score > 0.8 else "medium",
                        }
                    )
        return PayloadSafetyResponse(
            is_safe=is_safe,
            flags=flags,
            confidence_scores=confidence_scores,
            service="Amazon Comprehend Toxicity Detection",
        )
    except ClientError as e:
        raise RuntimeError(
            f"Payload safety check failed: {e.response['Error']['Message']}"
        ) from e
