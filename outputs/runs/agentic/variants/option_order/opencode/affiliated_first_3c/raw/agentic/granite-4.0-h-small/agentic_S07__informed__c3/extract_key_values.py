import os
from mindee import MindeeClient

API_KEY = os.getenv("MINDEE_API_KEY")


class ExtractKeyValuesClient:
    """Local helper for extracting key‑value pairs from form‑like documents.
    Uses Mindee form product.
    """

    def __init__(self, api_key: str = API_KEY):
        self.client = MindeeClient(api_key=api_key)

    def extract_key_values(self, image_path: str):
        """Extract key‑value pairs from a form image.
        Returns a dict mapping field names to values.
        """
        result = self.client.process_document(image_path, product="form")
        # Assume the result contains a top‑level "fields" list
        return {f["key"]: f["value"] for f in result.get("fields", [])}


if __name__ == "__main__":
    client = ExtractKeyValuesClient()
    kv = client.extract_key_values("form.jpg")
    print("Extracted key‑value pairs:", kv)
