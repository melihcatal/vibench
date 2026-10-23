import boto3


def safety_threshold(text, threshold):
    comprehend = boto3.client("comprehend")
    response = comprehend.detect_toxic_content(
        TextSegments=[{"Text": text}], LanguageCode="en"
    )
    if response["ResultList"][0]["ToxicityScore"] > threshold:
        return False
    return True
