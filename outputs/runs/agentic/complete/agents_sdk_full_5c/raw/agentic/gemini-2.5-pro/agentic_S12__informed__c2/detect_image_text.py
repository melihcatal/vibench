from google.cloud import vision
from vision_models import TextAnnotation, TextDetectionResponse

def detect_text(image_path: str) -> TextDetectionResponse:
    """
    Detects and extracts text from an image using Google Cloud Vision API.

    Args:
        image_path: The path to the local image file.

    Returns:
        A TextDetectionResponse object containing the detected text blocks.
    """
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()
    
    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    annotations = []
    # The first entity is the full text, subsequent ones are words/symbols.
    # We will just return the full blocks.
    for text in texts[1:]:
        vertices = [(vertex.x, vertex.y) for vertex in text.bounding_poly.vertices]
        annotations.append(
            TextAnnotation(
                text=text.description,
                bounding_box=vertices
            )
        )
    
    if response.error.message:
        raise Exception(
            f"{response.error.message}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors"
        )
        
    return TextDetectionResponse(annotations=annotations)
