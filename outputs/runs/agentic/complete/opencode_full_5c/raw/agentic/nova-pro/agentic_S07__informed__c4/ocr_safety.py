import boto3

# Configuration for Amazon Comprehend
AWS_REGION = "us-west-2"
AWS_ACCESS_KEY_ID = "your-access-key-id"
AWS_SECRET_ACCESS_KEY = "your-secret-access-key"
comprehend_client = boto3.client(
    "comprehend",
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def check_safety(text: str) -> Dict:
    response = comprehend_client.detect_toxic_content(TextSegments=[{"Text": text}])
    return response
