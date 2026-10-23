import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


OPENAI_API_BASE_URL = os.getenv("OPENAI_API_BASE_URL", "https://api.openai.com/v1")
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODEL = os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")


@dataclass(frozen=True)
class InvoiceNoteTranslationRequest:
    text: str
    target_language: str = "en"
    source_language: Optional[str] = None

    def to_payload(self) -> Dict[str, Any]:
        payload = {"text": self.text, "target_language": self.target_language}
        if self.source_language:
            payload["source_language"] = self.source_language
        return payload


@dataclass(frozen=True)
class InvoiceNoteTranslationResult:
    translated_text: str
    model: str
    raw: Optional[Dict[str, Any]] = None


class InvoiceNoteTranslationError(RuntimeError):
    pass


class InvoiceNoteTranslator:
    def __init__(self, api_key: Optional[str] = None, base_url: str = OPENAI_API_BASE_URL, model: str = OPENAI_MODEL, timeout: float = 30.0) -> None:
        self.api_key = api_key or os.getenv(OPENAI_API_KEY_ENV)
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout
        self._session = requests.Session()

    @property
    def headers(self) -> Dict[str, str]:
        if not self.api_key:
            raise InvoiceNoteTranslationError(f"Missing API key in {OPENAI_API_KEY_ENV}")
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def translate(self, text: str, target_language: str = "en", source_language: Optional[str] = None) -> InvoiceNoteTranslationResult:
        prompt = [
            f"Translate the following invoice note or description into {target_language}.",
            "Return only the translated text.",
        ]
        if source_language:
            prompt.append(f"Source language: {source_language}.")
        prompt.append(f"Text: {text}")
        response = self._session.post(
            f"{self.base_url}/responses",
            headers=self.headers,
            json={
                "model": self.model,
                "input": "\n".join(prompt),
            },
            timeout=self.timeout,
        )
        if response.status_code >= 400:
            raise InvoiceNoteTranslationError(f"{response.status_code} {response.text}")
        payload = response.json()
        translated_text = self._extract_text(payload)
        return InvoiceNoteTranslationResult(translated_text=translated_text, model=self.model, raw=payload)

    def _extract_text(self, payload: Dict[str, Any]) -> str:
        if isinstance(payload.get("output_text"), str) and payload["output_text"].strip():
            return payload["output_text"].strip()
        output = payload.get("output") or []
        for item in output:
            if not isinstance(item, dict):
                continue
            content = item.get("content") or []
            for piece in content:
                if isinstance(piece, dict):
                    text = piece.get("text") or piece.get("output_text")
                    if isinstance(text, str) and text.strip():
                        return text.strip()
        raise InvoiceNoteTranslationError("No translated text returned by provider")

    def close(self) -> None:
        self._session.close()
