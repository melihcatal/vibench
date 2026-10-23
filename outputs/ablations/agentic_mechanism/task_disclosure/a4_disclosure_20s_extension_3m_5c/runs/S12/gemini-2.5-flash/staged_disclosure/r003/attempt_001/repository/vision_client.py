import os
import io
import base64
from google.cloud import vision

# --- Configuration ---
# It's recommended to set GOOGLE_APPLICATION_CREDENTIALS environment variable
# or explicitly provide credentials when initializing the client.
# For local development, you might load from a .env file or similar.
# Example: GOOGLE_CLOUD_VISION_API_KEY = os.getenv("GOOGLE_CLOUD_VISION_API_KEY")

# --- Client Helper Utilities ---

def analyze_image_from_file(image_path: str, features: list[vision.Feature.Type]):
    """
    Analyzes an image from a local file path using Google Cloud Vision API.

    Args:
        image_path: The path to the image file.
        features: A list of vision.Feature.Type to request (e.g., TEXT_DETECTION, LABEL_DETECTION).

    Returns:
        A Google Cloud Vision API response object.
    """
    client = vision.ImageAnnotatorClient()

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    
    # Constructing the features list for the request
    vision_features = []
    for feature_type in features:
        vision_features.append(vision.Feature(type=feature_type))

    response = client.annotate_image({'image': image, 'features': vision_features})
    return response

def analyze_image_from_uri(image_uri: str, features: list[vision.Feature.Type]):
    """
    Analyzes an image from a publicly accessible URI using Google Cloud Vision API.

    Args:
        image_uri: The URI of the image (e.g., gs://bucket/image.jpg or http://example.com/image.jpg).
        features: A list of vision.Feature.Type to request (e.g., TEXT_DETECTION, LABEL_DETECTION).

    Returns:
        A Google Cloud Vision API response object.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(source=vision.ImageSource(image_uri=image_uri))

    # Constructing the features list for the request
    vision_features = []
    for feature_type in features:
        vision_features.append(vision.Feature(type=feature_type))

    response = client.annotate_image({'image': image, 'features': vision_features})
    return response

def analyze_image_from_base64(image_base64: str, features: list[vision.Feature.Type]):
    """
    Analyzes an image from a base64 encoded string using Google Cloud Vision API.

    Args:
        image_base64: The base64 encoded string of the image.
        features: A list of vision.Feature.Type to request (e.g., TEXT_DETECTION, LABEL_DETECTION).

    Returns:
        A Google Cloud Vision API response object.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=base64.b64decode(image_base64))

    # Constructing the features list for the request
    vision_features = []
    for feature_type in features:
        vision_features.append(vision.Feature(type=feature_type))

    response = client.annotate_image({'image': image, 'features': vision_features})
    return response

