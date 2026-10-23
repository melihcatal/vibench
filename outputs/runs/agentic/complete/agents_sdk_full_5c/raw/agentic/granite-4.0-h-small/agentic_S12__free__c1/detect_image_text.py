import vision_client

def detect_image_text(image_path):
    # Use Google Cloud Vision's OCR to detect any text inside the image
    # The `text_detection` method returns detected text in `text_annotations`
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as f:
        content = f.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = [annotation.description for annotation in response.text_annotations]
    return texts
