import boto3


def describe_image(image_path):
    client = boto3.client("rekognition")
    with open(image_path, "rb") as image:
        response = client.detect_labels(Image={"Bytes": image.read()})
    return " ".join([label["Name"] for label in response["Labels"]][:5])
