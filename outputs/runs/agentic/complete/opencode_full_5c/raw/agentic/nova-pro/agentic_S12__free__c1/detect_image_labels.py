import boto3

client = boto3.client("rekognition")


def detect_image_labels(image_path):
    with open(image_path, "rb") as image:
        response = client.detect_labels(Image={"Bytes": image.read()}, MaxLabels=10)
    return response["Labels"]
