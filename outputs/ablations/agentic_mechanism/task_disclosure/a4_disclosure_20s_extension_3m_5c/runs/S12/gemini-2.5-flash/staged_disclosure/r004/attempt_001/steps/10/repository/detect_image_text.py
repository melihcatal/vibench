from google.cloud import vision

def detect_text(image_path):
    """Detects text in the image using the Google Cloud Vision API."""
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        print(f"Text detected in {image_path}:")
        for text in texts:
            print(f"\nDescription: {text.description}")
            print(f"Bounds: {','.join([f'{v.x},{v.y}' for v in text.bounding_poly.vertices])}")
    else:
        print(f"No text detected in {image_path}.")

    if response.error.message:
        raise Exception(
            f"{response.error.message}"
        )

if __name__ == "__main__":
    # Replace 'path/to/your/image.jpg' with the actual path to your image file
    # For example: detect_text("your_image.jpg")
    # Make sure you have authenticated to Google Cloud and enabled the Vision AI API.
    print("Please provide an image path to the detect_text function.")
