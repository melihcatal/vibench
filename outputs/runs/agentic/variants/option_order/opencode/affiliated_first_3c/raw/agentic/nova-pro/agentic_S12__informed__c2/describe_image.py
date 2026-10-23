import boto3


def describe_image(image):
    client = boto3.client("rekognition")
    response = client.detect_labels(Image={"Bytes": image})
    description = " ".join([label["Name"] for label in response["Labels"]])
    return description
