import os
from google.cloud import vision

def describe_image(image_uri: str) -> str:
    """Generates a short visual description for an image using label detection."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]

    if labels:
        description = f"An image featuring {', '.join(labels[:3])}."
    else:
        description = "An image with no clear labels detected."
    
    return description

if __name__ == '__main__':
    # Example usage (replace with a valid image URI)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    image_uri = "gs://cloud-samples-data/vision/label/wakeupcat.jpg"
    print(f"Describing image {image_uri}:")
    description = describe_image(image_uri)
    print(description)
