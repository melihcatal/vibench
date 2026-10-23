import boto3
from typing import List, Dict, Any


def check_text_for_safety(text_content: str, aws_region: str = "us-east-1") -> Dict[str, Any]:
    """
    Moderates text content for safety using AWS Rekognition.
    """
    if not text_content:
        return {"is_safe": True, "labels": []}

    try:
        client = boto3.client("rekognition", region_name=aws_region)

        response = client.detect_moderation_labels(
            Image={"Bytes": b''}, # Not used for text, but required
            ProjectVersion='', # Not used for text, but required
            GeneralLabels={}, # Not used for text, but required
            HumanLoopConfig={}, # Not used for text, but required
            Content={"S3Object":{"Bucket":"","Name":""}}, # Use S3Object if text is in S3
            Text={"Content": text_content}
        )
        
        moderation_labels = response.get("ModerationLabels", [])
        
        if moderation_labels:
            return {
                "is_safe": False,
                "labels": [
                    {"name": label["Name"], "confidence": label["Confidence"]}
                    for label in moderation_labels
                ],
            }
        else:
            return {"is_safe": True, "labels": []}

    except Exception as e:
        # Handle potential AWS credentials errors or API issues
        return {"is_safe": False, "error": str(e)}
