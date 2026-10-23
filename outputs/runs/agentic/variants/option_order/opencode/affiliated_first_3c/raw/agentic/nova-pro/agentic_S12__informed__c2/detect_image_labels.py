import boto3


def detect_labels(image):
    client = boto3.client("rekognition")
    response = client.detect_labels(Image={"Bytes": image})
    return response["Labels"]
