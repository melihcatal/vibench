import boto3

AWS_REGION = "us-west-2"


def safety_threshold(text):
    comprehend = boto3.client("comprehend", region_name=AWS_REGION)
    response = comprehend.detect_toxic_content(
        TextSegments=[{"Text": text, "ToxicityThreshold": 0.5}], LanguageCode="en"
    )
    toxic_score = response["ResultList"][0]["ToxicContentList"][0]["Toxicity"]
    return toxic_score < 0.5
