import os
import json
from mindee import Document, MindeeClient


# Same-scenario scored file – extract table cells and row structure from a document
class ExtractTables:
    def __init__(self):
        self.api_key = os.getenv("MINDEE_API_KEY")
        if not self.api_key:
            raise RuntimeError("Set MINDEE_API_KEY")
        self.client = MindeeClient(self.api_key)

    def process(self, image_path: str):
        doc = Document.from_path(image_path)
        result = self.client.ocr.process(doc)
        tables = []
        for page in result.pages:
            for tbl in page.tables:
                rows = []
                for row in tbl.rows:
                    cells = [cell.text for cell in row.cells]
                    rows.append(cells)
                tables.append({"rows": rows})
        return tables


if __name__ == "__main__":
    extractor = ExtractTables()
    tables = extractor.process("sample.jpg")
    print("Extracted tables:", tables)
