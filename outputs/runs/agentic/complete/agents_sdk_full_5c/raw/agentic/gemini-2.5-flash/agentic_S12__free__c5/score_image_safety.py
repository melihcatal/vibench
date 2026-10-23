import os
from google.cloud import vision_v1p4beta1 as vision

def score_image_safety(image_uri: str):
    """Checks an image for unsafe or policy-sensitive visual content using Safe Search Detection."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.safe_search_detection(image=image)
    safe_search = response.safe_search_annotation

    safety_scores = {
        "adult": safe_search.adult.name,
        "spoof": safe_search.spoof.name,
        "medical": safe_search.medical.name,
        "violence": safe_search.violence.name,
        "racy": safe_search.racy.name,
    }
    return safety_scores

if __name__ == '__main__':
    # This is a placeholder for demonstration. In a real scenario, load from config or env.
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/credentials.json"
    
    # Example usage with a public image URI
    # safety_results = score_image_safety("gs://cloud-samples-data/vision/label/wakeupcat.jpg")
    # print("Image safety scores:", safety_results)
    pass
