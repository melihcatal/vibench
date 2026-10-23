import boto3


def check_visual_labels_safety(labels):
    client = boto3.client("comprehend")
    for label in labels:
        response = client.detect_toxic_content(Text=label["Name"], LanguageCode="en")
        if response["Labels"]:
            return False
    return True
