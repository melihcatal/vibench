import boto3


def moderate_transcript(transcript):
    client = boto3.client("comprehend")
    response = client.detect_toxic_content(
        TextSegments=[{"Text": transcript, "LanguageCode": "en"}], LanguageCode="en"
    )
    return response["ResultList"][0]["Labels"]
