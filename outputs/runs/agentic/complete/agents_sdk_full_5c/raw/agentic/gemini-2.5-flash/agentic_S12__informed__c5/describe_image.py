from google.cloud import vision
import os

def describe_image(image_content: bytes) -> str:
    """Generates a short visual description for an image using detected labels."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]

    if labels:
        # Simple concatenation for a description
        description = "This image appears to show: " + ", ".join(labels[:5]) + "."
        return description
    else:
        return "No specific visual elements could be clearly identified."

if __name__ == '__main__':
    # Example usage (requires an actual image binary)
    # For a real scenario, load image_content from a file or network
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/credentials.json"
    # with open("path/to/your/image.jpg", "rb") as image_file:
    #     content = image_file.read()
    #     description = describe_image(content)
    #     print(f"Image description: {description}")
    pass