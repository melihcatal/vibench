import os
from google.cloud import documentai


class GoogleDocumentAILayoutHelper:
    def __init__(self):
        # Use environment variable for credential configuration
        self.client = documentai.DocumentProcessorServiceClient()

    def extract_layout(self, uri: str):
        """Extract blocks, lines, tables, or other layout elements from a document using Google Document AI.

        Args:
            uri (str): URI or GCS URL of the document image.

        Returns:
            dict: Parsed layout information containing blocks, lines, and tables.
        """
        # Invoke processing and retrieve the first processed document
        result = self.client.process_document(
            request={
                "name": "projects/your-project/locations/us-central1/processors/your-processor-id",
                "input_config": {"gcs_source": {"uri": uri}},
            }
        )
        # Parse layout elements from the response (simplified illustrative output)
        layout = {
            "blocks": result.document.pages[0].layout.blocks,
            "lines": result.document.pages[0].layout.lines,
            "tables": result.document.pages[0].layout.tables,
        }
        return layout


def main():
    helper = GoogleDocumentAILayoutHelper()
    uri = "gs://your-bucket/document.png"
    layout = helper.extract_layout(uri)
    print("Extracted layout:", layout)


if __name__ == "__main__":
    main()
