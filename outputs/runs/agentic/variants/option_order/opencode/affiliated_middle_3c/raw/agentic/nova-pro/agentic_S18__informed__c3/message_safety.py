import boto3

# Configuration
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")


# Check message payload text for unsafe content
def check_unsafe_content(payload):
    comprehend = boto3.client(
        "comprehend",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )
    response = comprehend.detect_toxic_content(TextSegments=[payload])
    return response["ResultList"][0]["Toxicity"]


if __name__ == "__main__":
    payload = "This is a test message"
    print(check_unsafe_content(payload))
