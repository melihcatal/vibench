from google.cloud import vision
import os

def describe_image(image_content: bytes) -> str:
    """Generates a short visual description for an image using Google Cloud Vision label detection.
    This provides prominent labels, which can act as descriptive terms.
    For more narrative descriptions, object localization or web detection could also be used.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations if label.description]

    if labels:
        # Simple heuristic: join top labels to form a basic description
        return "An image depicting: " + ", ".join(labels[:5]) + "."
    else:
        return "No clear description found."

if __name__ == '__main__':
    print("Running describe_image.py example...")
    dummy_image_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0cIDATx\xda\xed\xc1\x01\x01\x00\x00\x00\xc2\xa0\xf7Om\x00\x00\x00\x00IEND\xaeB`\x82" # A tiny valid PNG
    
    description = describe_image(dummy_image_content)
    print("Image description:", description)
