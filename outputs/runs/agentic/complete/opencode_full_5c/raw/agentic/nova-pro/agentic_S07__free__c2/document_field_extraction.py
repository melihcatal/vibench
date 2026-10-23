import boto3


def extract_structured_fields(text):
    comprehend = boto3.client("comprehend")
    response = comprehend.detect_entities(Text=text, LanguageCode="en")
    return response["Entities"]
