# vision_client.py
# Helper utilities for the Static Image & Visual Understanding scenario

import os
from google.cloud import vision_v1 as vision
from PIL import Image

# Initialize a Vision API client (credentials loaded from GOOGLE_APPLICATION_CREDENTIALS env var)
client = vision.ImageAnnotatorClient()

# ----------------------------------------------------------------------------------------------
# Load an image from file and return a Vision API compatible `Image` object
# ----------------------------------------------------------------------------------------------
def load_image(image_path):
    """Open a local image file and wrap it in a Vision API `Image` object."""
    try:
        with Image.open(image_path).convert('RGB') as img:
            return vision.Image(content=img.tobytes())
    except Exception as exc:
        raise RuntimeError(f"Unable to load image {image_path}: {exc}")

# ----------------------------------------------------------------------------------------------
# LABEL DETECTION
# ----------------------------------------------------------------------------------------------
def detect_labels(image_path):
    """Detect labels/objects using the Vision API and return a list of label strings."""
    image = load_image(image_path)
    response = client.label_detection(image=image)
    return [anno.description for anno in response.label_annotations]

# ----------------------------------------------------------------------------------------------
# IMAGE DESCRIPTION (short visual caption)
# ----------------------------------------------------------------------------------------------
def describe_image(image_path):
    """Return a concise textual description of the image."""
    image = load_image(image_path)
    response = client.label_detection(image=image)
    if not response.label_annotations:
        return "No visual information could be extracted."
    # Simple heuristic: use the most confident label as a short caption
    return response.label_annotations[0].description

# ----------------------------------------------------------------------------------------------
# TEXT DETECTION (OCR)
# ----------------------------------------------------------------------------------------------
def detect_text(image_path):
    """OCR an image and return extracted text strings."""
    image = load_image(image_path)
    response = client.text_detection(image=image)
    texts = [anno.description for anno in response.text_annotations]
    return texts

# ----------------------------------------------------------------------------------------------
# SAFETY AND POLICY CHECK (unsafe, adult, violent, etc.)
# ----------------------------------------------------------------------------------------------
def score_safety(image_path):
    """Analyse safety annotations and return a list of flagged categories."""
    image = load_image(image_path)
    response = client.safe_search_detection(image=image)
    flags = []
    # Adult
    if response.safe_search_annotation.adult == vision.SafeSearchAnnotation.Adult.LIKELY:
        flags.append('adult')
    # Medical
    if response.safe_search_annotation.medical == vision.SafeSearchAnnotation.Medical.LIKELY:
        flags.append('medical')
    # Spoof
    if response.safe_search_annotation.spoof == vision.SafeSearchAnnotation.Spoof.LIKELY:
        flags.append('spoof')
    # Violence
    if response.safe_search_annotation.violence == vision.SafeSearchAnnotation.Violence.LIKELY:
        flags.append('violence')
    # Racy
    if response.safe_search_annotation.racy == vision.SafeSearchAnnotation.Racy.LIKELY:
        flags.append('racy')
    return flags

# ----------------------------------------------------------------------------------------------
# Example usage (uncomment to test)
# if __name__ == '__main__':
#     path = 'sample.jpg'
#     print('Labels:', detect_labels(path))
#     print('Caption:', describe_image(path))
#     print('Text:', detect_text(path))
#     print('Safety flags:', score_safety(path))
# ----------------------------------------------------------------------------------------------
