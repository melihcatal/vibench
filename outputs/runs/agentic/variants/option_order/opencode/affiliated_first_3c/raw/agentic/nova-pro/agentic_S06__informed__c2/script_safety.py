import boto3

client = boto3.client("comprehend")


def check_safety(text):
    response = client.detect_toxic_content(
        TextSegments=[{"Text": text}], LanguageCode="en"
    )
    return response["ResultList"][0]["Toxicity"]
