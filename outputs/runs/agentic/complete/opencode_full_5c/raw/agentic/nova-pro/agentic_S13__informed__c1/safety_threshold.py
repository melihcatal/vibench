import boto3

AWS_ACCESS_KEY_ID = "your_access_key_id"
AWS_SECRET_ACCESS_KEY = "your_secret_access_key"

comprehend = boto3.client(
    "comprehend",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name="us-east-1",
)


def safety_threshold(text, threshold=0.5):
    response = comprehend.detect_toxic_content(Text=text)
    if response["ToxicityScore"] > threshold:
        return False
    return True
