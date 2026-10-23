import boto3

client = boto3.client("rekognition")


def score_image_safety(image_path):
    with open(image_path, "rb") as image:
        response = client.detect_moderation_labels(Image={"Bytes": image.read()})
    return response["ModerationLabels"]
