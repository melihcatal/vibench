# safety_client.py
"""Local configuration and client helper utilities for Text Content Safety"""

import os
from typing import Dict, Any

# Provider selection – choose one concrete service
# Example: Azure AI Content Safety (REST)
PROVIDER = "azure"

if PROVIDER == "azure":
    AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    def build_request_payload(text: str, categories: list[str]) -> Dict[str, Any]:
        """Prepare request payload for Azure AI Content Safety (REST)"""
        return {
            "content": text,
            "categories": categories,
        }

    def parse_response(resp: Dict[str, Any]) -> Dict[str, Any]:
        """Extract moderation results from Azure response"""
        return {
            "unsafe_spans": resp.get("unsafe_spans"),
            "category_scores": resp.get("category_scores"),
        }

else:
    raise ValueError("Unsupported provider")
