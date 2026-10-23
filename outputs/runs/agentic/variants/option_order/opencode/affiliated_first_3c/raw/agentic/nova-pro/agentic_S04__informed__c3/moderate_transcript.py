import boto3

comprehend_client = boto3.client("comprehend")


def moderate_transcript(text):
    response = comprehend_client.detect_toxic_content(
        TextSegments=[{"Text": text}], LanguageCode="en"
    )
    return response["ResultList"][0]["Toxicity"]
