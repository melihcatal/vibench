import os
from mindee import MindeeClient

API_KEY = os.getenv("MINDEE_API_KEY")


class ExtractLayoutClient:
    """Local helper for layout extraction (blocks, lines, tables, etc.).
    Uses Mindee (generic) or Mindee specific products if available.
    """

    def __init__(self, api_key: str = API_KEY):
        self.client = MindeeClient(api_key=api_key)

    def extract_layout(self, image_path: str):
        """Extract layout elements from a document image.
        Returns a JSON-like dict with blocks, lines, tables, etc.
        """
        result = self.client.process_document(image_path, product="layout")
        return result


if __name__ == "__main__":
    client = ExtractLayoutClient()
    layout = client.extract_layout("sample.jpg")
    print("Layout extraction result:", layout)
