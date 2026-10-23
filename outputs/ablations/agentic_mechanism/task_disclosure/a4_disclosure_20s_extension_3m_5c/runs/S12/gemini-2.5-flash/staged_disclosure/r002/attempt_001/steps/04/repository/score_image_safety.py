from google.cloud import vision
import os

def score_image_safety(image_path):
    """Checks the image for unsafe or policy-sensitive visual content using Google Cloud Vision AI.

    Args:
        image_path: The path to the image file.

    Returns:
        A dictionary containing the safety attributes and their scores.
    """
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Loads the image into memory
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Performs label detection on the image
    response = client.safe_search_detection(image=image)
    safe_search_annotation = response.safe_search_annotation

    safety_scores = {
        'adult': safe_search_annotation.adult.name,
        'spoof': safe_search_annotation.spoof.name,
        'medical': safe_search_annotation.medical.name,
        'violence': safe_search_annotation.violence.name,
        'racy': safe_search_annotation.racy.name,
    }

    return safety_scores

if __name__ == '__main__':
    # Example usage: Replace 'path/to/your/image.jpg' with an actual image path
    # Ensure you have GOOGLE_APPLICATION_CREDENTIALS environment variable set
    # or authenticate your Google Cloud client library
    # For more details, refer to: https://cloud.google.com/docs/authentication/getting-started
    
    # You can create a dummy image for testing if you don't have one:
    # from PIL import Image
    # img = Image.new('RGB', (60, 30), color = 'red')
    # img.save('test_image.jpg')
    
    # Example using a placeholder. You would replace this with a real image path.
    # For the purpose of demonstration, let's assume 'test_image.jpg' exists.
    # If you run this without an image, it will raise an error.
    
    # This example requires an image file to exist at this path.
    # For a real application, you would ensure the file exists or handle the FileNotFoundError.
    
    # Let's try to create a dummy image for testing if it doesn't exist
    dummy_image_path = 'test_image.jpg'
    try:
        from PIL import Image
        if not os.path.exists(dummy_image_path):
            img = Image.new('RGB', (60, 30), color = 'blue')
            img.save(dummy_image_path)
            print(f"Created a dummy image at {dummy_image_path} for testing.")
    except ImportError:
        print("Pillow library not found. Please install it ('pip install Pillow') to create a dummy image for testing.")
        print("Skipping dummy image creation. Ensure 'test_image.jpg' exists or provide a valid image path.")
        
    if os.path.exists(dummy_image_path):
        print(f"Checking safety for image: {dummy_image_path}")
        try:
            safety_results = score_image_safety(dummy_image_path)
            print("Image Safety Scores:")
            for category, score in safety_results.items():
                print(f"  {category.capitalize()}: {score}")
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Please ensure you have authenticated with Google Cloud and have the Vision AI API enabled.")
            print("You can set GOOGLE_APPLICATION_CREDENTIALS environment variable to a service account key file path.")
            print("For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"")
    else:
        print(f"Error: Test image '{dummy_image_path}' not found. Please create it or provide a valid image path.")
