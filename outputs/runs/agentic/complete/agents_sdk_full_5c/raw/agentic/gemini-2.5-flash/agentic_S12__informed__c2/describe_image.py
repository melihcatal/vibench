from google.cloud import vision
import os

def describe_image(image_content: bytes) -> str:
    """Generates a short visual description for an image using Google Cloud Vision labels."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]

    if labels:
        # Combine top labels to form a simple description
        description = ", ".join(labels[:3]) # Take top 3 labels
        return f"The image depicts: {description}."
    else:
        return "No clear description could be generated."

if __name__ == '__main__':
    # Example usage (replace with actual image content)
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # For demonstration, assume a dummy image content
    dummy_image_content = b"fake_image_data_for_description"
    description = describe_image(dummy_image_content)
    print(f"Image description: {description}")
