import os
from google.cloud import vision

def score_image_safety(image_content: bytes) -> dict:
    """Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision Safe Search."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.safe_search_detection(image=image)
    safe_search_annotation = response.safe_search_annotation

    safety_scores = {
        "adult": safe_search_annotation.adult.name,
        "spoof": safe_search_annotation.spoof.name,
        "medical": safe_search_annotation.medical.name,
        "violence": safe_search_annotation.violence.name,
        "racy": safe_search_annotation.racy.name,
    }
    return safety_scores

if __name__ == '__main__':
    # Example usage (replace with actual image content)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # For demonstration, creating a dummy image content
    dummy_image_content = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\x0cIDATx\xda\xed\xc1\x01\x01\x00\x00\x00\xc2\xa0\xf7Om\x00\x00\x00\x00IEND\xaeB`\x82'

    try:
        safety_results = score_image_safety(dummy_image_content)
        print(f"Image Safety Scores: {safety_results}")
    except Exception as e:
        print(f"Error scoring image safety: {e}")
        print("Please ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set and points to a valid service account key file.")
