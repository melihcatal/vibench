import os
from mindee import MindeeClient

API_KEY = os.getenv("MINDEE_API_KEY")


class ExtractTablesClient:
    """Local helper for table extraction from documents.
    Uses Mindee table product.
    """

    def __init__(self, api_key: str = API_KEY):
        self.client = MindeeClient(api_key=api_key)

    def extract_tables(self, image_path: str):
        """Extract table cells and row structure from a document.
        Returns a JSON-like dict representing table layout.
        """
        result = self.client.process_document(image_path, product="table")
        return result


if __name__ == "__main__":
    client = ExtractTablesClient()
    tables = client.extract_tables("sample.jpg")
    print("Extracted tables:", tables)
