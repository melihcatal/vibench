
import os
from google.cloud import vision

def detect_image_labels(image_path):
    """Detects labels in the image file."""
    client = vision.ImageAnnotatorClient()

    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    
    return [{'description': label.description, 'score': label.score} for label in labels]

if __name__ == '__main__':
    # This is example usage and assumes you have an image file named 'test_image.jpg'
    # in the same directory and GOOGLE_APPLICATION_CREDENTIALS set up.
    # For a real application, consider passing the image content directly or
    # using a more robust argument parsing.
    
    # Replace 'path/to/your/image.jpg' with the actual path to your image
    # For demonstration, let's assume 'test_image.jpg' is available.
    # You would typically get this path from user input or other parts of your application.
    example_image_path = 'test_image.jpg' 
    
    if not os.path.exists(example_image_path):
        print(f"Please place a test image at {example_image_path} or update the path in the script.")
        print("Exiting as no image was found for demonstration.")
        exit()

    try:
        labels = detect_image_labels(example_image_path)
        if labels:
            print(f"Labels for {example_image_path}:")
            for label in labels:
                print(f"  {label['description']}: {label['score']:.2f}")
        else:
            print(f"No labels detected for {example_image_path}.")
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please ensure you have Google Cloud Vision API credentials set up.")
        print("For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"")
