
from google.cloud import vision

def summarize_image_analysis(image_path):
    """Summarizes visual analysis results for a given image using Google Cloud Vision AI.

    Args:
        image_path: The path to the image file.

    Returns:
        A string summarizing the analysis results.
    """
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Perform label detection
    response = client.label_detection(image=image)
    labels = response.label_annotations

    summary = f"Visual analysis results for {image_path}:
"
    if labels:
        summary += "Detected labels:
"
        for label in labels:
            summary += f"- {label.description} (score: {label.score:.2f})
"
    else:
        summary += "No labels detected.
"

    return summary

