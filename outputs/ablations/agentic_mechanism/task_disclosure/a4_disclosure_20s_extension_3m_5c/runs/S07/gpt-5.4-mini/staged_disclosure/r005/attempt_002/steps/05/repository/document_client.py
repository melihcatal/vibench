import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Any, Dict, Optional

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential


@dataclass(frozen=True)
class DocumentServiceConfig:
    endpoint: str
    api_key: str
    ocr_model_id: str = "prebuilt-read"
    layout_model_id: str = "prebuilt-layout"


def load_config(prefix: str = "DOC") -> DocumentServiceConfig:
    endpoint = os.getenv(f"{prefix}_DOCUMENT_INTELLIGENCE_ENDPOINT") or os.getenv(
        f"{prefix}_FORM_RECOGNIZER_ENDPOINT"
    )
    api_key = os.getenv(f"{prefix}_DOCUMENT_INTELLIGENCE_KEY") or os.getenv(
        f"{prefix}_FORM_RECOGNIZER_KEY"
    )
    if not endpoint or not api_key:
        raise ValueError("Missing Azure Document Intelligence configuration")
    ocr_model_id = os.getenv(f"{prefix}_OCR_MODEL_ID", "prebuilt-read")
    layout_model_id = os.getenv(f"{prefix}_LAYOUT_MODEL_ID", "prebuilt-layout")
    return DocumentServiceConfig(endpoint=endpoint, api_key=api_key, ocr_model_id=ocr_model_id, layout_model_id=layout_model_id)


@lru_cache(maxsize=1)
def get_document_analysis_client(prefix: str = "DOC") -> DocumentAnalysisClient:
    config = load_config(prefix)
    return DocumentAnalysisClient(config.endpoint, AzureKeyCredential(config.api_key))


def _analyze(path: str, model_id: str, prefix: str = "DOC") -> Any:
    client = get_document_analysis_client(prefix)
    with open(path, "rb") as f:
        poller = client.begin_analyze_document(model_id=model_id, document=f)
    return poller.result()


def analyze_ocr(path: str, prefix: str = "DOC") -> Any:
    return _analyze(path, load_config(prefix).ocr_model_id, prefix)


def analyze_layout(path: str, prefix: str = "DOC") -> Any:
    return _analyze(path, load_config(prefix).layout_model_id, prefix)


def extract_text(path: str, prefix: str = "DOC") -> str:
    result = analyze_ocr(path, prefix)
    if not getattr(result, "pages", None):
        return ""
    lines = []
    for page in result.pages:
        for line in getattr(page, "lines", []) or []:
            lines.append(line.content)
    return "\n".join(lines)


def extract_layout(path: str, prefix: str = "DOC") -> Dict[str, Any]:
    result = analyze_layout(path, prefix)
    pages = []
    for page in getattr(result, "pages", []) or []:
        pages.append(
            {
                "page_number": getattr(page, "page_number", None),
                "width": getattr(page, "width", None),
                "height": getattr(page, "height", None),
                "unit": getattr(page, "unit", None),
                "lines": [getattr(line, "content", "") for line in (getattr(page, "lines", []) or [])],
                "tables": len(getattr(result, "tables", []) or []),
            }
        )
    return {"pages": pages, "content": getattr(result, "content", "")}
