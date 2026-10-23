import os
import boto3
from botocore.exceptions import ClientError

# HELPER: document_client.py

# Provider: Amazon Textract (OCR/Layout)
# Credentials should be set via AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY


class DocumentClient:
    """Local helper client that abstracts Amazon Textract OCR/layout extraction.

    Provides convenience methods for extracting text, layout, tables, and key‑value pairs.
    """

    def __init__(self):
        self.textract = boto3.client("textract")
        # Optional: configure AWS region or profile if needed
        # self.textract = boto3.client('textract', region_name='us-east-1')

    def extract_text(self, image_bytes):
        """Extract plain text from a document image."""
        try:
            response = self.textract.detect_document_text(
                Document={"Bytes": image_bytes}
            )
        except ClientError as e:
            raise RuntimeError(f"Textract extraction error: {e}")
        text = "\n".join(
            item["Text"] for item in response["Blocks"] if item["BlockType"] == "LINE"
        )
        return text.strip()

    def extract_layout(self, image_bytes):
        """Extract layout elements (blocks, lines, tables)."""
        try:
            response = self.textract.analyze_document(
                Document={"Bytes": image_bytes}, FeatureTypes=["FORMS"]
            )
        except ClientError as e:
            raise RuntimeError(f"Textract layout extraction error: {e}")
        layout = {"blocks": [], "lines": [], "tables": []}
        for block in response.get("Blocks", []):
            if block["BlockType"] == "LINE":
                layout["lines"].append(block["Text"])
            elif block["BlockType"] == "TABLE":
                layout["tables"].append(block)
            else:
                layout["blocks"].append(block)
        return layout

    def extract_tables(self, image_bytes):
        """Extract tables and cell structures."""
        try:
            response = self.textract.analyze_document(
                Document={"Bytes": image_bytes}, FeatureTypes=["TABLES"]
            )
        except ClientError as e:
            raise RuntimeError(f"Textract tables extraction error: {e}")
        tables = []
        for block in response.get("Blocks", []):
            if block["BlockType"] == "TABLE":
                tables.append(self._build_table(block, response))
        return tables

    def _build_table(self, table_block, full_response):
        """Helper to construct a simplified table representation."""
        rows = []
        for row_block in full_response.get("Blocks", []):
            if row_block["BlockType"] == "CELL" and row_block.get("Relationships"):
                row_idx = row_block.get("RowIndex")
                col_idx = row_block.get("ColumnIndex")
                rows.append({"cell_index": (row_idx, col_idx), "content": ""})
        return {"rows": rows}

    def extract_key_values(self, image_bytes):
        """Extract key‑value pairs from a form‑like document."""
        try:
            response = self.textract.analyze_document(
                Document={"Bytes": image_bytes}, FeatureTypes=["FORMS"]
            )
        except ClientError as e:
            raise RuntimeError(f"Textract key‑value extraction error: {e}")
        kv = {}
        for block in response.get("Blocks", []):
            if block.get("BlockType") == "KEY_VALUE_SET":
                key = None
                value = None
                for rel in block.get("Relationships", []):
                    for id_info in rel.get("Ids", []):
                        if block.get("EntityTypes") and "KEY" in block.get(
                            "EntityTypes"
                        ):
                            key = self._get_block_text(id_info, full_response=response)
                        elif block.get("EntityTypes") and "VALUE" in block.get(
                            "EntityTypes"
                        ):
                            value = self._get_block_text(
                                id_info, full_response=response
                            )
                if key and value:
                    kv[key] = value
        return kv

    def _get_block_text(self, block_id, full_response):
        for block in full_response.get("Blocks", []):
            if block.get("Id") == block_id:
                return block.get("Text")
        return ""


# Example usage (uncomment to test):
# if __name__ == '__main__':
#     client = DocumentClient()
#     with open('sample.png', 'rb') as f:
#         img = f.read()
#     print(client.extract_text(img))
