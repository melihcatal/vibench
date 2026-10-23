from google.cloud import vision

def summarize_image(image_path):
    """Summarizes visual analysis results for a given image using Google Cloud Vision AI."""
    client = vision.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    summary = []
    if labels:
        for label in labels:
            summary.append(label.description)
    else:
        summary.append("No prominent labels found.")
            
    return ", ".join(summary)

