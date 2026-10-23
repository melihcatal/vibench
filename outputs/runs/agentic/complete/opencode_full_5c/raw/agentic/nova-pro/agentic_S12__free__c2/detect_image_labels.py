import boto3


def detect_labels(image_path):
    client = boto3.client("rekognition")
    with open(image_path, "rb") as image:
        response = client.detect_labels(Image={"Bytes": image.read()})
    return response["Labels"]
