
from google.cloud import vision
import os

def describe_image(image_path):
    """Generates a short visual description for an image using Google Cloud Vision AI."""
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # For local development, set this to the path of your service account key file.
    # Example: os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"

    client = vision.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations

    if labels:
        descriptions = [label.description for label in labels[:5]]  # Get top 5 descriptions
        return ", ".join(descriptions)
    else:
        return "No visual description found."

if __name__ == "__main__":
    # Example usage:
    # Replace 'your_image.jpg' with the actual path to your image file.
    # Make sure to set up GOOGLE_APPLICATION_CREDENTIALS environment variable
    # or uncomment and set the path in the describe_image function.
    image_file = "your_image.jpg" # Placeholder, user needs to provide a real image path
    
    # Create a dummy image file for demonstration purposes if it doesn't exist
    if not os.path.exists(image_file):
        print(f"Creating a dummy image file: {image_file}")
        try:
            from PIL import Image
            img = Image.new('RGB', (60, 30), color = 'red')
            img.save(image_file)
            print(f"Dummy image '{image_file}' created successfully.")
        except ImportError:
            print("Pillow library not found. Please install it (`pip install Pillow`) or provide an actual image file.")
            print("Skipping image description as no image file is available.")
            exit()

    description = describe_image(image_file)
    print(f"Description for {image_file}: {description}")
