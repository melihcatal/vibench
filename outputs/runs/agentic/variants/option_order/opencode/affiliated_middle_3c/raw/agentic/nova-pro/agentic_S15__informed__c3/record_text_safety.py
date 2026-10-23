import boto3

COMPREHEND_REGION = os.getenv("AWS_REGION")


def get_comprehend_client():
    return boto3.client("comprehend", region_name=COMPREHEND_REGION)


def check_text_safety(text):
    client = get_comprehend_client()
    response = client.detect_toxic_content(Text=text, LanguageCode="en")
    return response["Labels"][0]["Name"] == "Toxicity"
