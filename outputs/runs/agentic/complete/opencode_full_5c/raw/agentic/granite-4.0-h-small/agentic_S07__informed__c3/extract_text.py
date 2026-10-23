import os
import json
from mindee import Document, MindeeClient


# Same-scenario scored file – extract plain text from a scanned document image
class ExtractText:
    def __init__(self):
        # Mindee uses an API key environment variable
        self.api_key = os.getenv("MINDEE_API_KEY")
        if not self.api_key:
            raise RuntimeError("Set MINDEE_API_KEY environment variable")
        self.client = MindeeClient(self.api_key)

    def process(self, image_path: str) -> str:
        # Load image and send to Mindee OCR service
        doc = Document.from_path(image_path)
        result = self.client.ocr.process(doc)
        # Mindee returns structured fields; we flatten to plain text
        output = ""
        for page in result.pages:
            for line in page.lines:
                output += line.text + " "
        return output.strip()


if __name__ == "__main__":
    extractor = ExtractText()
    text = extractor.process("sample.jpg")
    print("Extracted text:", text)
