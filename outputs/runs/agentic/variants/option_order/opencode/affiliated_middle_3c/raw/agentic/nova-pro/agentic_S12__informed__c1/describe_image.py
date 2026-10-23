import boto3


def describe_image(image_path):
    rekognition_client = boto3.client("rekognition")
    with open(image_path, "rb") as image:
        response = rekognition_client.detect_labels(Image={"Bytes": image.read()})
    description = " ".join([label["Name"] for label in response["Labels"]])
    return description
