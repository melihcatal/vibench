import os
import json
from mindee import Document, MindeeClient


# Same-scenario scored file – extract layout blocks, lines, tables, etc. from a document
class ExtractLayout:
    def __init__(self):
        self.api_key = os.getenv("MINDEE_API_KEY")
        if not self.api_key:
            raise RuntimeError("Set MINDEE_API_KEY")
        self.client = MindeeClient(self.api_key)

    def process(self, image_path: str):
        doc = Document.from_path(image_path)
        result = self.client.ocr.process(doc)
        # Return a simplified representation of layout elements
        layout = {
            "blocks": [],
            "lines": [],
            "tables": [],
        }
        for page in result.pages:
            layout["blocks"].extend(page.blocks)
            layout["lines"].extend(page.lines)
            layout["tables"].extend(page.tables)
        return layout


if __name__ == "__main__":
    extractor = ExtractLayout()
    layout = extractor.process("sample.jpg")
    print("Extracted layout:", layout)
