import os
from google.cloud import documentai


class GoogleDocumentAIHelper:
    def __init__(self):
        # Use the environment variable for credential configuration
        self.client = documentai.DocumentProcessorServiceClient()

    def extract_text(self, uri: str) -> str:
        """Extract plain text from a scanned document image stored at the given URI using Google Document AI.

        Args:
            uri (str): The URI or GCS URL to the document image (e.g., 'gs://bucket/file.png').

        Returns:
            str: Plain text extracted from the document.
        """
        name = (
            self.client.process_document(
                request={
                    "name": "projects/your-project/locations/us-central1/processors/your-processor-id",
                    "input_config": {"gcs_source": {"uri": uri}},
                }
            )
            .text_annotations[0]
            .text
        )
        return name


def main():
    helper = GoogleDocumentAIHelper()
    # Example usage
    uri = "gs://your-bucket/document.png"
    plain_text = helper.extract_text(uri)
    print("Extracted text:\n", plain_text)


if __name__ == "__main__":
    main()
