import boto3


def score_safety(image):
    client = boto3.client("rekognition")
    response = client.detect_moderation_labels(Image={"Bytes": image})
    return response["ModerationLabels"]
