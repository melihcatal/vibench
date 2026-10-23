import os
from typing import Any, Dict

# Local helper – central client configuration for OCR & layout services
# Provides a simple factory to instantiate providers using env vars


class DocumentClient:
    SUPPORTED_SERVICES = {
        "mindee": {
            "class": "mindee.MindeeClient",
            "required": ["MINDEE_API_KEY"],
        },
        "amazon_textract": {
            "class": "boto3.client('textract')",
            "required": ["AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY"],
        },
    }

    @staticmethod
    def get_provider(service_name: str, **kwargs) -> Any:
        cfg = DocumentClient.SUPPORTED_SERVICES.get(service_name)
        if not cfg:
            raise ValueError(f"Unsupported service {service_name}")
        cls_path = cfg["class"]
        required = cfg["required"]
        for req in required:
            if not os.getenv(req):
                raise RuntimeError(f"Missing env var {req} for {service_name}")
        # Dynamically import & instantiate (simple example using Mindee)
        if cfg["class"].startswith("mindee."):
            from mindee import MindeeClient

            return MindeeClient(os.getenv("MINDEE_API_KEY"))
        elif cfg["class"].startswith("boto3."):
            import boto3

            return boto3.client(
                "textract",
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            )
        else:
            raise NotImplementedError(
                f"Instantiation for {cfg['class']} not implemented"
            )

    @staticmethod
    def normalize_response(raw: Dict[str, Any]) -> Dict[str, Any]:
        # Basic normalization: flatten nested structures to a common shape
        normalized = {
            "text": "",
            "layout": {},
            "tables": [],
            "key_values": {},
        }
        # Example: if raw comes from Mindee, pull out text and layout
        if isinstance(raw, dict) and "pages" in raw:
            for page in raw["pages"]:
                normalized["text"] += " ".join(
                    line["text"] for line in page.get("lines", [])
                )
                normalized["layout"] = {
                    "blocks": page.get("blocks", []),
                    "lines": page.get("lines", []),
                    "tables": page.get("tables", []),
                }
                normalized["tables"].extend(
                    [tbl["rows"] for tbl in page.get("tables", [])]
                )
                normalized["key_values"].update(
                    {
                        kv["key"]["text"]: kv["value"]["text"]
                        for kv in page.get("fields", [])
                        if kv.get("type") == "key_value"
                    }
                )
        return normalized

    @staticmethod
    def parse_response(raw: Dict[str, Any]) -> Dict[str, Any]:
        return DocumentClient.normalize_response(raw)


# Example usage (for testing)
if __name__ == "__main__":
    client = DocumentClient.get_provider("mindee")
    # Mock a Mindee response for demonstration
    mock = {
        "pages": [
            {
                "lines": [{"text": "Invoice No: 12345"}],
                "blocks": [],
                "tables": [],
                "fields": [
                    {
                        "type": "key_value",
                        "key": {"text": "Date"},
                        "value": {"text": "2025-01-01"},
                    },
                ],
            }
        ]
    }
    print(DocumentClient.parse_response(mock))
