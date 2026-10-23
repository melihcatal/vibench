from google.cloud import vision
import os

def score_image_safety(image_content: bytes) -> dict:
    """Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision Safe Search."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.safe_search_detection(image=image)
    safe_search_annotation = response.safe_search_annotation

    safety_scores = {
        "adult": safe_search_annotation.adult.name,
        "medical": safe_search_annotation.medical.name,
        "violence": safe_search_annotation.violence.name,
        "racy": safe_search_annotation.racy.name,
        "spoof": safe_search_annotation.spoof.name,
    }
    return safety_scores

if __name__ == '__main__':
    # Example usage (replace with actual image content)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # For demonstration, assume a dummy image content
    dummy_image_content = b"fake_image_data_for_safety_score"
    safety_results = score_image_safety(dummy_image_content)
    print(f"Image safety scores: {safety_results}")
