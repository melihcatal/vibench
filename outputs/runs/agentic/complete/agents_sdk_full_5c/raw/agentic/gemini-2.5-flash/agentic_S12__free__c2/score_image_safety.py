from google.cloud import vision

def score_image_safety(image_content: bytes):
    """Checks an image for unsafe content using Google Cloud Vision API Safe Search."""
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
    # This is placeholder content for demonstration purposes.
    # In a real scenario, you would load an actual image.
    dummy_image_content = b"fake image data"
    print(f"Image safety scores: {score_image_safety(dummy_image_content)}")
