import os
from typing import Any, Dict, List
from google.cloud import documentai

# Common configuration for Google Document AI
PROJECT_ID = "your-project"
LOCATION = "us-central1"
PROCESSOR_ID = "your-processor-id"


class DocumentClient:
    """
    Thin wrapper to configure Google Document AI client and provide helper methods for OCR and layout extraction.
    """

    def __init__(self):
        self.client = documentai.DocumentProcessorServiceClient()

    def process_document(self, gcs_uri: str, return_raw: bool = False):
        """
        Process a document image stored in GCS using Document AI.

        Args:
            gcs_uri (str): Google Cloud Storage URI for the document image.
            return_raw (bool): Whether to return raw API response (default False).

        Returns:
            dict or google.cloud.documentai.types.document.Document: Processed document data.
        """
        name = self.client.process_document(
            request={
                "name": f"projects/{PROJECT_ID}/locations/{LOCATION}/processors/{PROCESSOR_ID}",
                "input_config": {"gcs_source": {"uri": gcs_uri}},
            }
        ).document

        return name if return_raw else name

    def extract_text(self, gcs_uri: str) -> str:
        """Extract plain text from the processed document."""
        doc = self.process_document(gcs_uri)
        return doc.pages[0].text_annotation.text

    def extract_layout(self, gcs_uri: str) -> Dict[str, Any]:
        """Extract layout blocks, lines, and tables."""
        doc = self.process_document(gcs_uri)
        return {
            "blocks": [b for b in doc.pages[0].layout.blocks],
            "lines": [l for l in doc.pages[0].layout.lines],
            "tables": [t for t in doc.pages[0].layout.tables],
        }

    def extract_tables(self, gcs_uri: str) -> List[Dict[str, Any]]:
        """Extract table cells and row structure."""
        doc = self.process_document(gcs_uri)
        tables = []
        for table in doc.pages[0].layout.tables:
            t = {
                "header": [cell.text for cell in table.header_cells],
                "rows": [
                    [cell.text for cell in row_cells] for row_cells in table.body_rows
                ],
            }
            tables.append(t)
        return tables

    def extract_key_values(self, gcs_uri: str) -> List[Dict[str, str]]:
        """Extract key-value pairs from form-like documents."""
        doc = self.process_document(gcs_uri)
        key_values = []
        for kv in doc.pages[0].layout.key_value_pairs:
            key_values.append({"key": kv.key.text, "value": kv.value.text})
        return key_values


def main():
    client = DocumentClient()
    uri = "gs://your-bucket/document.png"
    # Example usage
    text = client.extract_text(uri)
    layout = client.extract_layout(uri)
    tables = client.extract_tables(uri)
    kv_pairs = client.extract_key_values(uri)
    print(text[:200])
    print(layout)
    print(tables[:2])
    print(kv_pairs[:2])


if __name__ == "__main__":
    main()
