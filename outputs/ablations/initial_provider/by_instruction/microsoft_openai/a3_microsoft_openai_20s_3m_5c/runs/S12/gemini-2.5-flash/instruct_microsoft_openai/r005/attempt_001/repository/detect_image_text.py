from vision_client import VisionClient
from vision_models import ImageInput, ImageTextDetectionResponse, DetectedText
from google.cloud import vision_v1p3beta1 as vision # Ensure this import matches vision_client

def detect_image_text(image_input: ImageInput) -> ImageTextDetectionResponse:
    client = VisionClient()
    google_vision_client = client.get_google_vision_client()

    image = vision.Image()
    if image_input.image_url:
        image.source.image_uri = image_input.image_url
    elif image_input.image_base64:
        image.content = image_input.image_base64
    else:
        raise ValueError("Either image_url or image_base64 must be provided.")

    response = google_vision_client.text_detection(image=image)
    
    detected_texts = []
    if response.text_annotations:
        # The first annotation is the aggregated text for the entire image
        # Subsequent annotations are for individual words/lines
        for annotation in response.text_annotations:
            vertices = []
            for vertex in annotation.bounding_poly.vertices:
                vertices.extend([vertex.x, vertex.y])
            detected_texts.append(DetectedText(text=annotation.description, bounding_boxes=vertices))
            
    return ImageTextDetectionResponse(texts=detected_texts)