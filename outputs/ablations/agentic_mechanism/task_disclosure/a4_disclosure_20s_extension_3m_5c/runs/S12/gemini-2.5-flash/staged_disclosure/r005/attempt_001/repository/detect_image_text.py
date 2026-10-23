from google.cloud import vision

def detect_text(image_path_or_uri):
    """Detects text in the image file or at the given URI."""
    client = vision.ImageAnnotatorClient()

    if image_path_or_uri.startswith("gs://") or image_path_or_uri.startswith("http://") or image_path_or_uri.startswith("https://"):
        image = vision.Image()
        image.source.image_uri = image_path_or_uri
    else:
        with open(image_path_or_uri, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    if texts:
        # The first annotation is the overall text detected
        full_text = texts[0].description
        print(f"Full text: {full_text}")
    else:
        print("No text detected.")

    for i, text in enumerate(texts[1:], 1):  # Skip the first full text annotation
        print(f"Text {i}: {text.description}")
        print(f"Bounds: {','.join([f'{v.x_coordinate},{v.y_coordinate}' for v in text.bounding_poly.vertices])}")

    if response.error.message:
        raise Exception(
            f'{response.error.message}
For more info on error messages, check: '
            f'https://cloud.google.com/apis/design/errors'
        )

if __name__ == '__main__':
    # Replace with your image path or URI (e.g., "path/to/your/image.jpg", "gs://your-bucket/your-image.jpg")
    # Make sure you have authenticated to Google Cloud and enabled the Vision AI API.
    # For local files, ensure the file exists.
    # For URIs, ensure public accessibility or appropriate permissions.
    image_to_process = "path/to/your/image.jpg" # Placeholder
    detect_text(image_to_process)
