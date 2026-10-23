import boto3

client = boto3.client("rekognition")


def describe_image(image_path):
    with open(image_path, "rb") as image:
        response = client.detect_labels(Image={"Bytes": image.read()}, MaxLabels=1)
    return (
        response["Labels"][0]["Name"]
        if response["Labels"]
        else "No description available"
    )
