import os
from google.cloud import vision_v1p4beta1 as vision

def detect_image_labels(image_uri: str):
    """Detects labels in the image located in Google Cloud Storage or a web URI."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.label_detection(image=image)
    labels = [label.description for label in response.label_annotations]
    return labels

if __name__ == '__main__':
    # This is a placeholder for demonstration. In a real scenario, load from config or env.
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/credentials.json"
    
    # Example usage with a public image URI
    # labels = detect_image_labels("gs://cloud-samples-data/vision/label/wakeupcat.jpg")
    # print("Labels detected:", labels)
    pass
