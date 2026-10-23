# extract_tables.py
# SAME-SCENARIO implementation file

# Using Amazon Textract for table extraction
import boto3
from document_client import TableExtractionClient


class AmazonTextractTableClient(TableExtractionClient):
    def __init__(self, region_name="us-east-1"):
        self.client = boto3.client(
            service_name="textract",
            region_name=region_name,
            # credentials are provided via environment variables
            # AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
        )

    def extract(self, image_bytes):
        response = self.client.analyze_document(
            Document={"Bytes": image_bytes}, FeatureTypes=["TABLES"]
        )
        # Gather table cells
        table_data = []
        for block in response["Blocks"]:
            if block["BlockType"] == "CELL":
                table_data.append(
                    {
                        "row_index": block["RowIndex"],
                        "column_index": block["ColumnIndex"],
                        "text": block.get("Text", ""),
                    }
                )
        return table_data


# Example usage (not executed here)
# client = AmazonTextractTableClient()
# tables = client.extract(open('sample.pdf', 'rb').read())
# print(tables)
