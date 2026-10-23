from google.cloud import vision
import os

def score_image_safety(image_content: bytes) -> dict:
    """Checks an image for unsafe or policy-sensitive visual content."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

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
    # Example usage (requires an actual image binary)
    # For a real scenario, load image_content from a file or network
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/credentials.json"
    # with open("path/to/your/image.jpg", "rb") as image_file:
    #     content = image_file.read()
    #     safety_results = score_image_safety(content)
    #     print(f"Safety results: {safety_results}")
    pass