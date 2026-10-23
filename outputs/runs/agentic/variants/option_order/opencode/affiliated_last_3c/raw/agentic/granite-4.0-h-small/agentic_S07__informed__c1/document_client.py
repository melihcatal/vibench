import os
from typing import Any, Dict

# Local helper: abstraction over OCR/layout providers
# This module loads credentials and returns a generic client
# Example provider: Amazon Textract (identified by boto3 client creation)


def load_aws_credentials() -> Dict[str, str]:
    """Load AWS credentials from environment variables."""
    return {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
    }


class DocumentClient:
    """
    Generic client that delegates to a concrete OCR/layout service.
    Currently only implements Amazon Textract as the reference provider.
    """

    def __init__(self):
        creds = load_aws_credentials()
        self.client = self._create_textract_client(**creds)

    def _create_textract_client(
        self, aws_access_key_id: str, aws_secret_access_key: str
    ):
        import boto3

        return boto3.client(
            "textract",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    def extract_text(self, image_bytes: bytes) -> str:
        """Extract plain text using the underlying provider."""
        client = self.client
        response = client.detect_document_text(Document={"Bytes": image_bytes})
        return " ".join(
            item["Text"] for item in response["Blocks"] if item["BlockType"] == "LINE"
        )

    def extract_layout(self, image_bytes: bytes) -> dict:
        """Extract layout (blocks, lines, tables) using the provider."""
        client = self.client
        response = client.analyze_document(
            Document={"Bytes": image_bytes}, FeatureTypes=["FORMS"]
        )
        layout = {"lines": [], "tables": [], "other": []}
        for item in response.get("Blocks", []):
            block_type = item.get("BlockType")
            if block_type == "LINE":
                layout["lines"].append(item.get("Text"))
            elif block_type == "TABLE":
                layout["tables"].append(item)
            else:
                layout["other"].append(item)
        return layout

    def extract_tables(self, image_bytes: bytes) -> list:
        """Extract tables only."""
        client = self.client
        response = client.analyze_document(
            Document={"Bytes": image_bytes}, FeatureTypes=["TABLES"]
        )
        tables = []
        for table in response.get("Blocks", []):
            if table.get("BlockType") != "TABLE":
                continue
            cells = []
            for cell in table.get("Relationships", []):
                if cell.get("Type") != "CHILD":
                    continue
                for field in cell.get("Ids", []):
                    cell_block = next(
                        (b for b in response["Blocks"] if b["Id"] == field), None
                    )
                    if cell_block and cell_block.get("BlockType") == "CELL":
                        text = next(
                            (
                                b["Text"]
                                for b in response["Blocks"]
                                if b["Id"]
                                == cell_block.get("Relationships", [{}])[0].get(
                                    "Ids", [{}]
                                )[0]
                            ),
                            "",
                        )
                        cells.append(text)
            tables.append(cells)
        return tables

    def extract_key_values(self, image_bytes: bytes) -> dict:
        """Extract key-value pairs using the provider."""
        client = self.client
        response = client.analyze_document(
            Document={"Bytes": image_bytes}, FeatureTypes=["FORMS"]
        )
        kv = {}
        for item in response.get("Blocks", []):
            if item.get("BlockType") == "KEY_VALUE_SET":
                rel = item.get("Relationships", [])
                key = next((b.get("Text") for b in rel if b.get("Type") == "KEY"), "")
                value = next(
                    (b.get("Text") for b in rel if b.get("Type") == "VALUE"), ""
                )
                if key and value:
                    kv[key] = value
        return kv
