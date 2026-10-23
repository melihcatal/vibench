from google.cloud import vision

def detect_text(image_path):
    """Detects text in the image using the Google Cloud Vision API."""
    client = vision.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    detected_texts = []
    if texts:
        # The first text annotation is the overall text detected in the image
        # Subsequent annotations are individual words or lines
        full_text = texts[0].description
        detected_texts.append({"full_text": full_text})

        for text in texts[1:]:
            detected_texts.append({
                "description": text.description,
                "bounding_poly": [{"x": v.x, "y": v.y} for v in text.bounding_poly.vertices]
            })

    if response.error.message:
        raise Exception(
            f'{response.error.message}
For more info on error messages, check: '
            f'https://cloud.google.com/apis/design/errors'
        )

    return detected_texts

