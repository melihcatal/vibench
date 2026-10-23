import os
from google.cloud import documentai


class GoogleDocumentAITableHelper:
    def __init__(self):
        # Use environment variable for credential configuration
        self.client = documentai.DocumentProcessorServiceClient()

    def extract_tables(self, uri: str):
        """Extract table cells and row structure from a document using Google Document AI.

        Args:
            uri (str): URI or GCS URL of the document image.

        Returns:
            list[dict]: List of tables with cells and row data.
        """
        # Invoke processing and retrieve the document
        result = self.client.process_document(
            request={
                "name": "projects/your-project/locations/us-central1/processors/your-processor-id",
                "input_config": {"gcs_source": {"uri": uri}},
            }
        )
        tables = []
        for table_annotations in result.document.pages[0].layout.tables:
            table = {
                "header": [cell.text for cell in table_annotations.header_cells],
                "rows": [
                    [cell.text for cell in row_cells]
                    for row_cells in table_annotations.body_rows
                ],
            }
            tables.append(table)
        return tables


def main():
    helper = GoogleDocumentAITableHelper()
    uri = "gs://your-bucket/document.png"
    tables = helper.extract_tables(uri)
    print("Extracted tables:", tables)


if __name__ == "__main__":
    main()
