import os
from google.cloud import vision_v1p4beta1 as vision

def detect_image_text(image_uri: str):
    """Detects text in the image located in Google Cloud Storage or a web URI."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = image_uri

    response = client.text_detection(image=image)
    texts = [text.description for text in response.text_annotations]
    
    if texts:
        # The first annotation is the aggregated text from the entire image
        return texts[0]
    return ""

if __name__ == '__main__':
    # This is a placeholder for demonstration. In a real scenario, load from config or env.
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/credentials.json"
    
    # Example usage with a public image URI with text
    # text = detect_image_text("gs://cloud-samples-data/vision/text/screen.jpg")
    # print("Text detected:", text)
    pass
