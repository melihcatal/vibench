
import os
from google.cloud import vision_v1p3beta1 as vision

def score_image_safety(image_path):
    """
    Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision AI.
    """
    client = vision.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.safe_search_detection(image=image)
    safe_search_annotation = response.safe_search_annotation

    print(f"Safe Search results for {image_path}:")
    print(f"Adult: {vision.Likelihood(safe_search_annotation.adult).name}")
    print(f"Medical: {vision.Likelihood(safe_search_annotation.medical).name}")
    print(f"Racy: {vision.Likelihood(safe_search_annotation.racy).name}")
    print(f"Spoof: {vision.Likelihood(safe_search_annotation.spoof).name}")
    print(f"Violence: {vision.Likelihood(safe_search_annotation.violence).name}")

    return safe_search_annotation

if __name__ == "__main__":
    # Replace with the actual path to your image
    _image_path = "path/to/your/image.jpg"
    if os.path.exists(_image_path):
        score_image_safety(_image_path)
    else:
        print(f"Error: Image not found at {_image_path}. Please update _image_path with a valid image file.")
        print("You can install the Google Cloud Vision client library using: pip install google-cloud-vision")
        print("Also, ensure you have authenticated your Google Cloud application (e.g., using `gcloud auth application-default login`)")
