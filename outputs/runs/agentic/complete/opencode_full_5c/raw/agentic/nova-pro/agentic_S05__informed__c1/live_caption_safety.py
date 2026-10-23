import boto3


def live_caption_safety(text):
    comprehend = boto3.client(
        "comprehend",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    result = comprehend.detect_toxic_content(Text=text)
    return result.get("Labels")
