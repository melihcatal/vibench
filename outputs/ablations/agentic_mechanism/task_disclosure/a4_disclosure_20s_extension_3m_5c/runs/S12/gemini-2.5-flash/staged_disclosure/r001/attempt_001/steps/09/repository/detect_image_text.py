import os
from google.cloud import vision

def detect_text(image_path):
    """Detects text in the image file."""
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print("Texts:")

    for text in texts:
        print(f'\n"{text.description}"')

    if response.error.message:
        raise Exception(
            "{}
For more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )

if __name__ == "__main__":
    # Replace 'path/to/your/image.jpg' with the actual path to your image file
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
    # authenticate using other methods as described in Google Cloud Vision API documentation.
    # Example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    
    # You can provide the image path as a command-line argument,
    # or modify this line to point to your image.
    image_file_path = "path/to/your/image.jpg" 
    # For demonstration, you might want to create a dummy image or provide a real path.
    # Example: image_file_path = "image.jpg" 

    if os.path.exists(image_file_path):
        detect_text(image_file_path)
    else:
        print(f"Error: Image file not found at '{image_file_path}'. Please update the image_file_path variable.")
