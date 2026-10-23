import os
import json
from mindee import Document, MindeeClient


# Same-scenario scored file – extract key-value pairs from a form-like document
class ExtractKeyValues:
    def __init__(self):
        self.api_key = os.getenv("MINDEE_API_KEY")
        if not self.api_key:
            raise RuntimeError("Set MINDEE_API_KEY")
        self.client = MindeeClient(self.api_key)

    def process(self, image_path: str):
        doc = Document.from_path(image_path)
        result = self.client.ocr.process(doc)
        kv_pairs = {}
        for page in result.pages:
            for field in page.fields:
                if field.type == "key_value":
                    kv_pairs[field.key.text] = field.value.text
        return kv_pairs


if __name__ == "__main__":
    extractor = ExtractKeyValues()
    kv = extractor.process("sample.jpg")
    print("Extracted key-value pairs:", kv)
