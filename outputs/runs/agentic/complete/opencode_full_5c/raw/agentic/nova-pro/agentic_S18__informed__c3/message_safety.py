import boto3


# Check message payload text for unsafe content
def check_message_safety(message):
    comprehend_client = boto3.client("comprehend")
    response = comprehend_client.detect_toxic_content(
        Text=message["Message"], LanguageCode="en"
    )
    return response["Labels"]
