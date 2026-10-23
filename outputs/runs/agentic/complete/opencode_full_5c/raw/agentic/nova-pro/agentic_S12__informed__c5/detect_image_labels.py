import boto3


def detect_image_labels(image_path):
    rekognition = boto3.client("rekognition")
    with open(image_path, "rb") as image:
        response = rekognition.detect_labels(Image={"Bytes": image.read()})
    return response["Labels"]
