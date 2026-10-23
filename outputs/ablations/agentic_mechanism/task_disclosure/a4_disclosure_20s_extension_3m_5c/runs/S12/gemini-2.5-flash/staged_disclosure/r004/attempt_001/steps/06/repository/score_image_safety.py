import os
from google.cloud import vision

def score_image_safety(image_path):
    """Checks an image for unsafe or policy-sensitive visual content using Google Cloud Vision AI."""

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Loads the image into memory
    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Performs safe search detection on the image feature
    response = client.safe_search_detection(image=image)
    safe_search = response.safe_search_annotation

    # Prepare results
    safety_scores = {
        "adult": safe_search.adult,
        "medical": safe_search.medical,
        "racy": safe_search.racy,
        "violence": safe_search.violence,
        "spoof": safe_search.spoof,
    }

    # Helper to convert likelihood enum to a readable string
    likelihood_name = (
        "UNKNOWN",
        "VERY_UNLIKELY",
        "UNLIKELY",
        "POSSIBLE",
        "LIKELY",
        "VERY_LIKELY",
    )

    readable_scores = {k: likelihood_name[v] for k, v in safety_scores.items()}

    return readable_scores

if __name__ == "__main__":
    # Example usage: Replace with your image path
    # Make sure to set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    # e.g., export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"
    
    # Create a dummy image for testing purposes
    dummy_image_path = "dummy_image.jpg"
    try:
        from PIL import Image
        img = Image.new('RGB', (60, 30), color = 'red')
        img.save(dummy_image_path)
    except ImportError:
        print("Pillow not installed. Please install it (`pip install Pillow`) or provide a real image file.")
        exit()

    if os.path.exists(dummy_image_path):
        print(f"Checking safety for image: {dummy_image_path}")
        scores = score_image_safety(dummy_image_path)
        print("Image safety scores:")
        for category, score in scores.items():
            print(f"- {category.capitalize()}: {score}")
        os.remove(dummy_image_path) # Clean up the dummy image
    else:
        print(f"Error: Image file not found at {dummy_image_path}")
        print("Please provide a valid image path or ensure a dummy image can be created.")
