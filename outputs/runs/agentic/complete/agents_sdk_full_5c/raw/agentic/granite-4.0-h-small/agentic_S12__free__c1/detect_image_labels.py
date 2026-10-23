import vision_client

def detect_image_labels(image_path):
    # Use Google Cloud Vision to detect labels/objects in the image
    # Google Cloud Vision provides label detection via the `labelAnnotations` field
    from google.cloud import vision  # provider-specific import
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as f:
        content = f.read()
    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = [annotation.description for annotation in response.label_annotations]
    return labels
