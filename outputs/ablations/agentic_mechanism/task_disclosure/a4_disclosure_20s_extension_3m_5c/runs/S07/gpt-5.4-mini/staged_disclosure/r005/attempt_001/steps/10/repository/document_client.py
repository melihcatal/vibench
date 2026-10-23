import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class DocumentServiceConfig:
    ocr_api_base: str = os.getenv("OCR_API_BASE", "https://api.ocr.space/parse/image")
    layout_api_base: str = os.getenv("LAYOUT_API_BASE", "https://api.veryfi.com/api/v8/partner/documents")
    ocr_api_key: Optional[str] = os.getenv("OCR_API_KEY")
    layout_client_id: Optional[str] = os.getenv("LAYOUT_CLIENT_ID")
    layout_client_secret: Optional[str] = os.getenv("LAYOUT_CLIENT_SECRET")


class OCRClient:
    def __init__(self, config: Optional[DocumentServiceConfig] = None) -> None:
        self.config = config or DocumentServiceConfig()

    def extract_text(self, image_url: str, language: str = "eng") -> Dict[str, Any]:
        headers = {}
        if self.config.ocr_api_key:
            headers["apikey"] = self.config.ocr_api_key
        response = requests.post(
            self.config.ocr_api_base,
            headers=headers,
            data={"url": image_url, "language": language, "isOverlayRequired": False},
            timeout=60,
        )
        response.raise_for_status()
        return response.json()


class LayoutExtractionClient:
    def __init__(self, config: Optional[DocumentServiceConfig] = None) -> None:
        self.config = config or DocumentServiceConfig()

    def extract_layout(self, file_bytes: bytes, filename: str) -> Dict[str, Any]:
        if not self.config.layout_client_id or not self.config.layout_client_secret:
            raise ValueError("LAYOUT_CLIENT_ID and LAYOUT_CLIENT_SECRET are required")
        response = requests.post(
            self.config.layout_api_base,
            auth=(self.config.layout_client_id, self.config.layout_client_secret),
            files={"file": (filename, file_bytes)},
            timeout=60,
        )
        response.raise_for_status()
        return response.json()


def get_document_services() -> Dict[str, Any]:
    config = DocumentServiceConfig()
    return {"ocr": OCRClient(config), "layout_extraction": LayoutExtractionClient(config), "config": config}
