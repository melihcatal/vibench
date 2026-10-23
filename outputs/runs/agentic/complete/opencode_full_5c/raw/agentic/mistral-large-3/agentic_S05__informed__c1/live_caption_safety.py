import os
import boto3
from typing import AsyncGenerator, Dict, Any

def check_unsafe_content(
    text_stream: AsyncGenerator[str, None], None
) -> AsyncGenerator[Dict[str, Any], None]:
    """
    Checks live transcript text for unsafe content using Amazon Comprehend.
    """
    comprehend_client = boto3.client(
        "comprehend",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name="us-east-1"
    )

    async for text in text_stream:
        response = comprehend_client.detect_toxic_content(
            TextSegments=[{"Text": text}],
            LanguageCode="en"
        )
        
        toxicity_scores = response["ResultList"][0]["ToxicityScores"]
        is_unsafe = any(score > 0.7 for score in toxicity_scores.values())
        
        yield {
            "text": text,
            "is_unsafe": is_unsafe,
            "toxicity_scores": toxicity_scores
        }