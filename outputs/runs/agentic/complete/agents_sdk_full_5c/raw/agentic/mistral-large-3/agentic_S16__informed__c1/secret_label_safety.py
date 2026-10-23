import boto3
import os

def secret_label_safety(label_text: str) -> dict:
    client = boto3.client(
        service_name='comprehend',
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    
    response = client.detect_toxic_content(
        TextSegments=[{"Text": label_text}],
        LanguageCode="en"
    )
    
    return {
        "toxicity_score": response["ResultList"][0]["Toxicity"]
    }