import boto3

AWS_ACCESS_KEY_ID = "your_access_key_id"
AWS_SECRET_ACCESS_KEY = "your_secret_access_key"

comprehend = boto3.client(
    "comprehend",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name="us-east-1",
)


def redact_unsafe(text):
    response = comprehend.detect_toxic_content(Text=text)
    redacted_text = text
    for item in response["ToxicContentItems"]:
        redacted_text = (
            redacted_text[: item["BeginOffset"]]
            + "[REDACTED]"
            + redacted_text[item["EndOffset"] :]
        )
    return redacted_text
