# [HELPER] document_client.py
"""Local configuration and client utilities for OCR / Layout Extraction providers"""

import os
from typing import Any, Dict, Optional


# Example configuration - can be loaded from environment, .env, or a config file
class OCRConfig:
    def __init__(self, region: str = "us-east-1") -> None:
        self.region = region
        self.endpoint_url: Optional[str] = os.getenv("OCR_ENDPOINT_URL")

    def get_client(self, service: str = "textract") -> Any:
        """Create a provider client (here using AWS Textract as example)"""
        if service == "textract":
            import boto3

            client_kwargs: Dict[str, Any] = {"region_name": self.region}
            if self.endpoint_url:
                client_kwargs["endpoint_url"] = self.endpoint_url
            return boto3.client(service_name=service, **client_kwargs)
        raise ValueError(f"Unsupported service: {service}")


# Singleton example (optional)
def get_ocr_client() -> Any:
    """Return a configured OCR client"""
    cfg = OCRConfig()
    return cfg.get_client()


if __name__ == "__main__":
    # Simple test harness
    client = get_ocr_client()
    print("Configured OCR client:", client)
