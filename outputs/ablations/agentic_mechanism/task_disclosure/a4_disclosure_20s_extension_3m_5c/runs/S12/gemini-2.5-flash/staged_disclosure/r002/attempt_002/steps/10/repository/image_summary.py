
from google.cloud import vision
import os

def summarize_image(image_path):
    """
    Summarizes the visual content of an image using Google Cloud Vision AI.
    """
    # Instantiates a client for Google Cloud Vision AI
    client = vision.ImageAnnotatorClient()

    # Loads the image from the specified path
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Performs label detection on the image
    response = client.label_detection(image=image)
    labels = response.label_annotations

    summary_parts = []
    if labels:
        summary_parts.append("The image contains:")
        for label in labels:
            summary_parts.append(f"- {label.description} (score: {label.score:.2f})")
    else:
        summary_parts.append("Could not detect any labels in the image.")

    # You can add more features like OCR, face detection, etc.
    # For example, to detect text (OCR):
    # response_text = client.text_detection(image=image)
    # texts = response_text.text_annotations
    # if texts:
    #     summary_parts.append("
Detected text:")
    #     for text in texts:
    #         summary_parts.append(f"- {text.description}")

    return "\n".join(summary_parts)

if __name__ == '__main__':
    # This is an example of how to use the function.
    # Replace 'path/to/your/image.jpg' with the actual path to an image file.
    # Make sure you have authenticated your Google Cloud client.
    # For example, by setting the GOOGLE_APPLICATION_CREDENTIALS environment variable.
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    # Example usage (uncomment and replace with a valid image path to test)
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # example_image_path = os.path.join(current_dir, 'example.jpg') # Assuming example.jpg is in the same directory

    # if os.path.exists(example_image_path):
    #     print(f"Summarizing image: {example_image_path}")
    #     summary = summarize_image(example_image_path)
    #     print("\n--- Image Summary ---")
    #     print(summary)
    # else:
    #     print(f"Please place an image file (e.g., 'example.jpg') in {current_dir} or update 'image_path' to a valid image file to run this example.")
    print("This script provides a function to summarize images using Google Cloud Vision AI.")
    print("To use it, call the 'summarize_image' function with the path to your image.")
    print("Ensure you have authenticated with Google Cloud (e.g., via GOOGLE_APPLICATION_CREDENTIALS).")

