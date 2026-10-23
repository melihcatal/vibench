from typing import List, Dict, Any

class DocumentRequest:
    def __init__(self, image_content: bytes):
        self.image_content = image_content

class TextExtractionResponse:
    def __init__(self, text: str, full_response: Dict[str, Any]):
        self.text = text
        self.full_response = full_response
