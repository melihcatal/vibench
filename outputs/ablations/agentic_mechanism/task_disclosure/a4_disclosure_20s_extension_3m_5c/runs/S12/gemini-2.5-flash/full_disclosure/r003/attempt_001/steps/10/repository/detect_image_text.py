from google.cloud import vision_v1
import os

def detect_text_in_image(image_path: str):
    """Detects text in the image located in the local file system or a GCS URI.
    
    Args:
        image_path: The path to the image file or a Google Cloud Storage URI (e.g., "gs://cloud-samples-data/vision/label/wakeupcat.jpg")
    
    Returns:
        A list of texts found in the image.
    """
    
    client = vision_v1.ImageAnnotatorClient()

    if image_path.startswith("gs://"):
        image = vision_v1.Image()
        image.source.image_uri = image_path
    else:
        with open(image_path, 'rb') as image_file:
            content = image_file.read()
        image = vision_v1.Image(content=content)

    response = client.text_detection(image=image)
    texts = [text.description for text in response.text_annotations]

    return texts

if __name__ == '__main__':
    # Example usage (replace with a valid image path or GCS URI)
    # For local file:
    # image_file = "path/to/your/image.jpg" 
    # For GCS URI:
    # image_gcs_uri = "gs://cloud-samples-data/vision/text/sign.jpg"
    
    # print(f"Detected text in local image: {detect_text_in_image(image_file)}")
    # print(f"Detected text in GCS image: {detect_text_in_image(image_gcs_uri)}")
    pass
