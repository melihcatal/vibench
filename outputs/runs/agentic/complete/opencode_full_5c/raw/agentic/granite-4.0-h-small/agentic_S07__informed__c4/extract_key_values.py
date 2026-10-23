import os
from google.cloud import documentai


class GoogleDocumentAIKeyValueHelper:
    def __init__(self):
        # Use environment variable for credential configuration
        self.client = documentai.DocumentProcessorServiceClient()

    def extract_key_values(self, uri: str):
        """Extract key-value pairs from a form-like document using Google Document AI.

        Args:
            uri (str): URI or GCS URL of the document image.

        Returns:
            list[dict]: List of extracted key-value pairs.
        """
        result = self.client.process_document(
            request={
                "name": "projects/your-project/locations/us-central1/processors/your-processor-id",
                "input_config": {"gcs_source": {"uri": uri}},
            }
        )
        key_values = []
        for kv in result.document.pages[0].layout.key_value_pairs:
            key_values.append({"key": kv.key.text, "value": kv.value.text})
        return key_values


def main():
    helper = GoogleDocumentAIKeyValueHelper()
    uri = "gs://your-bucket/form.png"
    kv_pairs = helper.extract_key_values(uri)
    print("Extracted key-value pairs:", kv_pairs)


if __name__ == "__main__":
    main()
