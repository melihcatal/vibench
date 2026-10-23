import boto3

AWS_REGION = "us-west-2"


def moderate_text(text):
    comprehend = boto3.client("comprehend", region_name=AWS_REGION)
    response = comprehend.detect_toxic_content(
        TextSegments=[{"Text": text, "ToxicityThreshold": 0.5}], LanguageCode="en"
    )
    return response
