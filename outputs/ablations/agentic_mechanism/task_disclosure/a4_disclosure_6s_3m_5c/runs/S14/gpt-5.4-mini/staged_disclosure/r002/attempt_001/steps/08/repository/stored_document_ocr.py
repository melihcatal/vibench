import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


@dataclass(frozen=True)
class StoredDocumentOCRResult:
    text: str
    raw: Dict[str, Any]


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise ValueError(f"{name} must be set")
    return value


def _build_document_url(bucket: str, key: str, region: str) -> str:
    return f"https://{bucket}.s3.{region}.amazonaws.com/{key.lstrip('/')}"


def run_ocr_on_stored_document(bucket: str, key: str, api_key: Optional[str] = None, region: Optional[str] = None) -> StoredDocumentOCRResult:
    assemblyai_api_key = api_key or _require_env("ASSEMBLYAI_API_KEY")
    aws_region = region or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-1"
    document_url = _build_document_url(bucket, key, aws_region)
    headers = {"authorization": assemblyai_api_key, "content-type": "application/json"}
    upload_response = requests.post("https://api.assemblyai.com/v2/upload", headers={"authorization": assemblyai_api_key}, json={"url": document_url}, timeout=60)
    upload_response.raise_for_status()
    audio_url = upload_response.json().get("upload_url") or upload_response.json().get("url") or document_url
    transcript_response = requests.post("https://api.assemblyai.com/v2/transcript", headers=headers, json={"audio_url": audio_url, "punctuate": True, "format_text": True}, timeout=60)
    transcript_response.raise_for_status()
    transcript_id = transcript_response.json()["id"]
    poll_url = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    while True:
        poll_response = requests.get(poll_url, headers={"authorization": assemblyai_api_key}, timeout=60)
        poll_response.raise_for_status()
        payload = poll_response.json()
        status = payload.get("status")
        if status == "completed":
            return StoredDocumentOCRResult(text=payload.get("text", ""), raw=payload)
        if status == "error":
            raise RuntimeError(payload.get("error", "AssemblyAI OCR failed"))


def main() -> None:
    bucket = _require_env("STORAGE_BUCKET")
    key = _require_env("STORED_DOCUMENT_KEY")
    result = run_ocr_on_stored_document(bucket=bucket, key=key)
    print(result.text)


if __name__ == "__main__":
    main()
