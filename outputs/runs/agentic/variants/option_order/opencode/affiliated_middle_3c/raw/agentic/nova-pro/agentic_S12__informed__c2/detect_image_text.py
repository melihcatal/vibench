import boto3

# Initialize the client
client = boto3.client("rekognition")


def detect_image_text(image_path):
    with open(image_path, "rb") as image:
        image_bytes = image.read()
        response = client.detect_text(Image={"Bytes": image_bytes})
        return response["TextDetections"]
