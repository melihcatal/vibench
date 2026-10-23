from google.cloud import vision

class DocumentClient:
    def __init__(self, project_id: str):
        self.client = vision.ImageAnnotatorClient()
        self.project_id = project_id

    def detect_text(self, image_content: bytes):
        """Performs text detection on the image content."""
        image = vision.Image(content=image_content)
        response = self.client.text_detection(image=image)
        texts = [text.description for text in response.text_annotations]
        return texts

    def detect_document_text(self, image_content: bytes):
        """Performs document text detection on the image content, including layout."""
        image = vision.Image(content=image_content)
        response = self.client.document_text_detection(image=image)
        return response.full_text_annotation
