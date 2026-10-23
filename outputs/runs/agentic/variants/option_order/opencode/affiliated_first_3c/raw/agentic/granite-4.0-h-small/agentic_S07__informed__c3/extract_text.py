import os
from mindee import MindeeClient

# Load credentials from environment
API_KEY = os.getenv("MINDEE_API_KEY")


class ExtractTextClient:
    """Local helper for generic OCR text extraction.
    Uses Mindee as the concrete provider.
    """

    def __init__(self, api_key: str = API_KEY):
        self.client = MindeeClient(api_key=api_key)

    def extract_text(self, image_path: str) -> str:
        """Extract plain text from a scanned document image.
        Args:
            image_path: Path to a local .jpg/.png image.
        Returns:
            Extracted plain text string.
        """
        result = self.client.process_document(image_path)
        # Assume Mindee returns JSON with a "text" field
        return result.get("text", "")


if __name__ == "__main__":
    # Example usage
    client = ExtractTextClient()
    text = client.extract_text("sample.jpg")
    print("Extracted text:", text)
