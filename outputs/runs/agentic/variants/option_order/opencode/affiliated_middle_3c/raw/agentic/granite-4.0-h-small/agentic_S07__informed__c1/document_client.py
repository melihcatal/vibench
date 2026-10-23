import os
import boto3


class DocumentClient:
    """Local helper client that provides configuration and utility methods for OCR/layout providers."""

    def __init__(self):
        # Example local configuration - in practice these would be loaded from env vars or config files
        self.region = os.getenv("AWS_REGION", "us-east-1")

    def normalize_textract_response(self, textract_resp: dict) -> dict:
        """Convert raw Amazon Textract response into a simplified structure."""
        full_text = "\n".join(
            block["Text"]
            for block in textract_resp.get("Blocks", [])
            if block["BlockType"] == "LINE"
        )
        return {"FullText": full_text}

    def normalize_textract_layout(self, textract_resp: dict) -> list:
        """Extract blocks, lines, and tables into a unified layout list."""
        layout = []
        for block in textract_resp.get("Blocks", []):
            block_type = block["BlockType"]
            if block_type == "KEY_VALUE_SET":
                layout.append(
                    {
                        "type": "key_value",
                        "id": block.get("Id"),
                        "text": block.get("Text", ""),
                    }
                )
            elif block_type == "LINE":
                layout.append({"type": "line", "text": block.get("Text", "")})
            elif block_type == "TABLE":
                rows = []
                for relation in block.get("Relations", []):
                    if relation["Type"] == "CHILD":
                        for child_id in relation["Ids"]:
                            child = next(
                                (
                                    b
                                    for b in textract_resp["Blocks"]
                                    if b["Id"] == child_id and b["BlockType"] == "CELL"
                                ),
                                None,
                            )
                            if child:
                                rows.append(child.get("Text", ""))
                layout.append({"type": "table", "rows": rows})
        return layout

    def normalize_textract_key_values(self, textract_resp: dict) -> list:
        """Extract key-value pairs from Textract FORMS output."""
        kv_pairs = []
        for block in textract_resp.get("Blocks", []):
            if block["BlockType"] == "KEY_VALUE_SET":
                key = next(
                    (
                        b["Text"]
                        for b in textract_resp["Blocks"]
                        if b["Id"] == block.get("Key", {}).get("Id")
                    ),
                    "",
                )
                value = next(
                    (
                        b["Text"]
                        for b in textract_resp["Blocks"]
                        if b["Id"] == block.get("Value", {}).get("Id")
                    ),
                    "",
                )
                kv_pairs.append({"key": key, "value": value})
        return kv_pairs
