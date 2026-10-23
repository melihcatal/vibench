from google.cloud import vision

class DescribeImageRequest:
    def __init__(self, image_bytes: bytes):
        self.image_bytes = image_bytes

class DescribeImageResponse:
    def __init__(self, description: str):
        self.description = description

def describe_image(request: DescribeImageRequest) -> DescribeImageResponse:
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=request.image_bytes)
    response = client.label_detection(image=image)
    labels = response.label_annotations

    if labels:
        description = ", ".join([label.description for label in labels])
    else:
        description = "No description found."

    return DescribeImageResponse(description=description)
