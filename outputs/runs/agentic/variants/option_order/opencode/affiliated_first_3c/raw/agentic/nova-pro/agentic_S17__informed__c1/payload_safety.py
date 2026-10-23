import boto3


def check_decrypted_payload(plaintext):
    comprehend = boto3.client("comprehend")
    response = comprehend.detect_toxic_content(Text=plaintext, LanguageCode="en")
    return response["Toxicity"]
