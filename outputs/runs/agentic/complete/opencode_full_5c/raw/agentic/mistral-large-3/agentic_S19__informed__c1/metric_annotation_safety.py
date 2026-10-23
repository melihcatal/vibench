import os
from typing import Dict, List, Optional

import boto3
from botocore.exceptions import ClientError


class MetricAnnotationSafetyChecker:
    def __init__(self):
        self.comprehend = boto3.client(
            "comprehend",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    def check_unsafe_text(self, text: str) -> Dict:
        try:
            response = self.comprehend.detect_toxic_content(
                TextSegments=[{"Text": text}], LanguageCode="en"
            )
            toxicity_scores = response["ResultList"][0]["ToxicityScores"]
            return {
                "is_toxic": any(score > 0.7 for score in toxicity_scores),
                "toxicity_scores": toxicity_scores,
                "categories": response["ResultList"][0]["Labels"],
            }
        except ClientError as e:
            return {
                "error": str(e),
                "is_toxic": False,
                "toxicity_scores": [],
                "categories": [],
            }

    def batch_check_unsafe_texts(self, texts: List[str]) -> List[Dict]:
        try:
            text_segments = [{"Text": text} for text in texts]
            response = self.comprehend.detect_toxic_content(
                TextSegments=text_segments, LanguageCode="en"
            )
            results = []
            for result in response["ResultList"]:
                toxicity_scores = result["ToxicityScores"]
                results.append(
                    {
                        "is_toxic": any(score > 0.7 for score in toxicity_scores),
                        "toxicity_scores": toxicity_scores,
                        "categories": result["Labels"],
                    }
                )
            return results
        except ClientError as e:
            return [{"error": str(e), "is_toxic": False}] * len(texts)
