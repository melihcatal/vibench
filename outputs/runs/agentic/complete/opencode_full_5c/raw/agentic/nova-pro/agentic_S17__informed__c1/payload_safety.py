import boto3


def check_decrypted_payload(decrypted_text):
    comprehend = boto3.client("comprehend")
    response = comprehend.detect_toxic_content(Text=decrypted_text, LanguageCode="en")
    return response["Labels"]
