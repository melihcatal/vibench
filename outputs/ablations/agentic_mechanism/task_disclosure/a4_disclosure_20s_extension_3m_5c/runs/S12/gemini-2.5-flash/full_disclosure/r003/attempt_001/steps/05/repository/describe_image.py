from google.cloud import vision
import os

def describe_image(image_path: str) -> str:
    """Generates a short visual description for an image using Google Cloud Vision AI.

    Args:
        image_path: The path to the image file.

    Returns:
        A string describing the image.
    """
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Loads the image into memory
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Performs label detection on the image
    response = client.label_detection(image=image)
    labels = response.label_annotations

    description_parts = []
    if labels:
        description_parts.append("The image shows:")
        for i, label in enumerate(labels):
            description_parts.append(f"{label.description}")
            if i < len(labels) - 1:
                description_parts.append(",")
    
    # Simple aggregation of labels to form a description
    return " ".join(description_parts).replace(" ,", ",") + "." if description_parts else "No clear description could be generated for the image."

if __name__ == '__main__':
    # Example usage (replace with a real image path)
    # Ensure you have GOOGLE_APPLICATION_CREDENTIALS set up
    # or pass credentials explicitly to ImageAnnotatorClient
    
    # Create a dummy image file for demonstration if it doesn't exist
    dummy_image_path = "dummy_image.jpg"
    if not os.path.exists(dummy_image_path):
        try:
            from PIL import Image
            img = Image.new('RGB', (60, 30), color = 'red')
            img.save(dummy_image_path)
            print(f"Created a dummy image at {dummy_image_path}")
        except ImportError:
            print("Pillow not installed. Cannot create dummy image. Please install it (`pip install Pillow`) or provide an existing image.")
            # If Pillow is not installed, we can't create a dummy image, so we skip the example
            print("Skipping example usage due to missing Pillow library or dummy image.")
            dummy_image_path = None

    if dummy_image_path and os.path.exists(dummy_image_path):
        print(f"Describing image: {dummy_image_path}")
        description = describe_image(dummy_image_path)
        print(description)
        # Clean up dummy image
        os.remove(dummy_image_path)
        print(f"Removed dummy image at {dummy_image_path}")
    else:
        print("Please provide a valid image path to test the function.")

