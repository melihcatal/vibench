import os
from google.cloud import vision

def describe_image(image_path: str) -> str:
    """Generates a short visual description for an image using Google Cloud Vision API.

    Args:
        image_path: The path to the image file.

    Returns:
        A string containing the description of the image.
    """
    client = vision.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    description_parts = [label.description for label in labels]
    if description_parts:
        return ", ".join(description_parts)
    else:
        return "No description found for the image."

if __name__ == '__main__':
    # This is an example usage. Replace 'path/to/your/image.jpg' with the actual image path.
    # Ensure you have authenticated to Google Cloud (e.g., by setting GOOGLE_APPLICATION_CREDENTIALS)
    # before running this script.
    # Example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    
    # Placeholder for image path - user needs to provide a real image path
    example_image_path = os.getenv("IMAGE_PATH", "path/to/your/image.jpg") 

    if example_image_path == "path/to/your/image.jpg":
        print("Please set the IMAGE_PATH environment variable or modify the script with the actual image path.")
    elif not os.path.exists(example_image_path):
        print(f"Error: Image file not found at {example_image_path}")
    else:
        print(f"Describing image: {example_image_path}")
        description = describe_image(example_image_path)
        print(f"Image description: {description}")
