import boto3


def detect_text(image):
    client = boto3.client("rekognition")
    response = client.detect_text(Image={"Bytes": image})
    return response["TextDetections"]
