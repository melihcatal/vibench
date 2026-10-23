# SAME-SCENARIO extract_layout.py

import os
from google.cloud import documentai_v1 as documentai  # Google Document AI SDK

# Load credentials from environment
PROJECT_ID = os.getenv("GOOGLE_PROJECT_ID")
LOCATION = os.getenv("GOOGLE_LOCATION", "us-central1")
DOCUMENT_AI_URI = os.getenv(
    "GOOGLE_DOCUMENTAI_URI", f"projects/{PROJECT_ID}/locations/{LOCATION}/processors"
)


class DocumentAIHelper:
    """Local helper to configure and call Google Document AI for layout extraction."""

    def __init__(self, creds_path: str):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path
        self.client = documentai.DocumentProcessorServiceClient()

    def process_document(self, image_path: str):
        """Process a scanned image and return layout blocks, lines, and tokens."""
        name = f"{DOCUMENT_AI_URI}/processor:process"
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()
        response = self.client.process_document(
            request={
                "name": name,
                "raw_document": {"content": image_bytes, "mime_type": "image/jpeg"},
            }
        )
        # Flatten layout elements into a readable structure
        layout = []
        for page in response.document.pages:
            for layout_elem in page.layout:
                layout.append(
                    {
                        "type": layout_elem.type,
                        "text": layout_elem.text,
                        "bounding_poly": layout_elem.bounding_poly.vertices,
                        "confidence": layout_elem.confidence,
                    }
                )
        return layout


if __name__ == "__main__":
    helper = DocumentAIHelper(creds_path="path/to/google-credentials.json")
    layout = helper.process_document("sample_document.jpg")
    print(f"Extracted {len(layout)} layout elements")
    # Uncomment to see the first few elements
    # for elem in layout[:5]:
    #     print(elem)
