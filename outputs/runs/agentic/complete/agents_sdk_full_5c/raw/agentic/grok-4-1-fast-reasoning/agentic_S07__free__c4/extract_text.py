from google.cloud import vision
from document_client import get_vision_client
from document_models import OCRText
import io

def extract_text(image_path: str) -> OCRText:
    client = get_vision_client()
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    text = texts[0].description if texts else ''
    return OCRText(text=text)