import boto3


def check_prompt_safety(text):
    client = boto3.client("comprehend")
    response = client.detect_toxic_content(
        TextSegments=[{"Text": text}], LanguageCode="en"
    )
    return response["ResultList"][0]["Toxicity"] > 0.5
