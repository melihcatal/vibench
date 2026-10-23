from google.cloud import vision
import os

def describe_image(image_uri: str, max_labels: int = 3):
    """Generates a short visual description for an image based on labels."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]

    if labels:
        # Construct a simple description from the top labels
        description_parts = labels[:max_labels]
        if len(description_parts) == 1:
            description = f"An image of {description_parts[0]}.".capitalize()
        elif len(description_parts) > 1:
            description = f"An image featuring {', '.join(description_parts[:-1])} and {description_parts[-1]}.".capitalize()
        else:
            description = "An image with no clear description."
    else:
        description = "No prominent objects or scenes detected."
    return description

if __name__ == '__main__':
    # This is an example, replace with a real image URI
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"
    image_uri = "gs://cloud-samples-data/vision/label/wakeupcat.jpg"
    description = describe_image(image_uri)
    print(f"Description for {image_uri}: {description}")

    image_uri_2 = "gs://cloud-samples-data/vision/text/screen.jpg"
    description_2 = describe_image(image_uri_2)
    print(f"Description for {image_uri_2}: {description_2}")
