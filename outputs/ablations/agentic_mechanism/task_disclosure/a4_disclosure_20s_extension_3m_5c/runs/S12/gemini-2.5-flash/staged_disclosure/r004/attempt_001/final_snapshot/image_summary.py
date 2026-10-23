import os
from google.cloud import vision

def summarize_image_analysis(image_path: str) -> dict:
    """Summarizes visual analysis results for a given image using Google Cloud Vision AI.

    Args:
        image_path: The path to the image file.

    Returns:
        A dictionary containing a summary of the image analysis, including labels,
        safe search attributes, and text (if detected).
    """
    client = vision.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.annotate_image({
        'image': image,
        'features': [
            {'type': vision.Feature.Type.LABEL_DETECTION},
            {'type': vision.Feature.Type.SAFE_SEARCH_DETECTION},
            {'type': vision.Feature.Type.TEXT_DETECTION},
        ]
    })

    summary = {}

    if response.label_annotations:
        labels = [label.description for label in response.label_annotations]
        summary['labels'] = labels

    if response.safe_search_annotation:
        safe_search = {
            'adult': vision.Likelihood(response.safe_search_annotation.adult).name,
            'spoof': vision.Likelihood(response.safe_search_annotation.spoof).name,
            'medical': vision.Likelihood(response.safe_search_annotation.medical).name,
            'violence': vision.Likelihood(response.safe_search_annotation.violence).name,
            'racy': vision.Likelihood(response.safe_search_annotation.racy).name,
        }
        summary['safe_search'] = safe_search

    if response.text_annotations:
        texts = [text.description for text in response.text_annotations]
        summary['full_text_annotation'] = response.full_text_annotation.text
        summary['detected_texts'] = texts

    return summary

if __name__ == '__main__':
    # Example usage:
    # Ensure you have GOOGLE_APPLICATION_CREDENTIALS set up
    # For more info: https://cloud.google.com/docs/authentication/getting-started
    
    # You would replace 'path/to/your/image.jpg' with an actual image path
    # For a local image, make sure it's accessible or provide a full path.
    # For demonstration purposes, we'll assume a dummy image path.
    dummy_image_path = "dummy_image.jpg" 
    
    # Create a dummy image file for demonstration if it doesn't exist
    if not os.path.exists(dummy_image_path):
        with open(dummy_image_path, "w") as f:
            f.write("This is a dummy image file content.")
        print(f"Created a dummy image file at: {dummy_image_path}")

    print(f"Summarizing analysis for {dummy_image_path}...")
    try:
        results = summarize_image_analysis(dummy_image_path)
        print("Image Analysis Summary:")
        print(results)
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure you have authenticated with Google Cloud and provided a valid image path.")
        print("For local testing, create a real image file or provide a valid path to an existing image.")
