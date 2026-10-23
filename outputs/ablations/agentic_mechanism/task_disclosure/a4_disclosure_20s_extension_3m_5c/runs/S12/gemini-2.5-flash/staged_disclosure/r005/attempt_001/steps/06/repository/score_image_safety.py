import os
from google.cloud import vision

def score_image_safety(image_path):
    """Detects unsafe or policy-sensitive visual content in an image using Google Cloud Vision AI."""

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Loads the image into memory
    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Performs label detection on the image
    response = client.safe_search_detection(image=image)
    safe_search = response.safe_search_annotation

    print(f"Safe search results for {image_path}:")
    print(f"Adult: {vision.Likelihood(safe_search.adult).name}")
    print(f"Medical: {vision.Likelihood(safe_search.medical).name}")
    print(f"Racy: {vision.Likelihood(safe_search.racy).name}")
    print(f"Spoof: {vision.Likelihood(safe_search.spoof).name}")
    print(f"Violence: {vision.Likelihood(safe_search.violence).name}")

    return {
        "adult": vision.Likelihood(safe_search.adult).name,
        "medical": vision.Likelihood(safe_search.medical).name,
        "racy": vision.Likelihood(safe_search.racy).name,
        "spoof": vision.Likelihood(safe_search.spoof).name,
        "violence": vision.Likelihood(safe_search.violence).name,
    }

if __name__ == "__main__":
    # Example usage:
    # To run this example, you need to have a test image.
    # Replace "path/to/your/image.jpg" with the actual path to your image file.
    # Make sure to set up Google Cloud authentication (e.g., GOOGLE_APPLICATION_CREDENTIALS)
    # For more information, visit: https://cloud.google.com/docs/authentication/getting-started
    # Ensure you have the 'google-cloud-vision' library installed: pip install google-cloud-vision

    # Create a dummy image file for demonstration purposes if it doesn't exist
    dummy_image_path = "dummy_image.jpg"
    if not os.path.exists(dummy_image_path):
        try:
            from PIL import Image
            img = Image.new('RGB', (60, 30), color = 'red')
            img.save(dummy_image_path)
            print(f"Created a dummy image at {dummy_image_path}")
        except ImportError:
            print("Pillow is not installed. Cannot create dummy image.")
            print("Please install Pillow: pip install Pillow")
            print("And create a dummy_image.jpg manually or provide a real image path.")
            exit()


    # Replace with your actual image path or use the dummy image
    image_to_check = dummy_image_path # "path/to/your/actual/image.jpg"
    if os.path.exists(image_to_check):
        score_image_safety(image_to_check)
    else:
        print(f"Error: Image file not found at {image_to_check}")
        print("Please provide a valid image path or ensure the dummy image is created.")

