from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Sequence

import requests

from document_models import OCRResult, as_lines, normalize_ocr_result


DEFAULT_OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
DEFAULT_OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com")


@dataclass(frozen=True)
class EmbeddingSection:
    text: str
    section_type: str = "text"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        payload = {"text": self.text, "section_type": self.section_type}
        if self.metadata:
            payload["metadata"] = dict(self.metadata)
        return payload


@dataclass(frozen=True)
class OpenAIEmbeddingConfig:
    api_key: str
    model: str = DEFAULT_OPENAI_EMBEDDING_MODEL
    api_base: str = DEFAULT_OPENAI_API_BASE
    timeout: float = 60.0


def load_openai_embedding_config(api_key: Optional[str] = None, model: Optional[str] = None, api_base: Optional[str] = None, timeout: Optional[float] = None) -> OpenAIEmbeddingConfig:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("Missing OpenAI API key")
    return OpenAIEmbeddingConfig(
        api_key=key,
        model=model or DEFAULT_OPENAI_EMBEDDING_MODEL,
        api_base=(api_base or DEFAULT_OPENAI_API_BASE).rstrip("/"),
        timeout=timeout or 60.0,
    )


def _normalize_sections(document: Any) -> List[EmbeddingSection]:
    if isinstance(document, OCRResult):
        return _sections_from_ocr_result(document)
    normalized = normalize_ocr_result(document)
    return _sections_from_ocr_result(normalized)


def _sections_from_ocr_result(result: OCRResult) -> List[EmbeddingSection]:
    sections: List[EmbeddingSection] = []
    if result.pages:
        for page in result.pages:
            if page.lines:
                for idx, line in enumerate(page.lines):
                    text = line.text.strip() or " ".join(word.text for word in line.words if word.text).strip()
                    if text:
                        sections.append(EmbeddingSection(text=text, section_type="line", metadata={"page_number": page.page_number, "line_index": idx}))
            elif page.text.strip():
                for idx, text in enumerate(as_lines(page.text)):
                    sections.append(EmbeddingSection(text=text, section_type="line", metadata={"page_number": page.page_number, "line_index": idx}))
    if not sections and result.text.strip():
        for idx, text in enumerate(as_lines(result.text)):
            sections.append(EmbeddingSection(text=text, section_type="text", metadata={"line_index": idx}))
    if not sections:
        sections.append(EmbeddingSection(text="", section_type="text", metadata={}))
    return sections


class OpenAIEmbeddingClient:
    def __init__(self, config: OpenAIEmbeddingConfig):
        self.config = config
        self.session = requests.Session()

    def embed_texts(self, texts: Sequence[str]) -> List[List[float]]:
        url = f"{self.config.api_base}/v1/embeddings"
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
        }
        response = self.session.post(url, json={"model": self.config.model, "input": list(texts)}, headers=headers, timeout=self.config.timeout)
        response.raise_for_status()
        data = response.json()
        embeddings = [item["embedding"] for item in sorted(data.get("data", []), key=lambda item: item.get("index", 0))]
        return [list(map(float, vector)) for vector in embeddings]


def create_embedding_client(api_key: Optional[str] = None, model: Optional[str] = None, api_base: Optional[str] = None, timeout: Optional[float] = None) -> OpenAIEmbeddingClient:
    return OpenAIEmbeddingClient(load_openai_embedding_config(api_key=api_key, model=model, api_base=api_base, timeout=timeout))


def embed_document_sections(document: Any, api_key: Optional[str] = None, model: Optional[str] = None, api_base: Optional[str] = None, timeout: Optional[float] = None) -> Dict[str, Any]:
    sections = _normalize_sections(document)
    client = create_embedding_client(api_key=api_key, model=model, api_base=api_base, timeout=timeout)
    vectors = client.embed_texts([section.text for section in sections])
    return {
        "model": client.config.model,
        "sections": [section.to_dict() for section in sections],
        "embeddings": [
            {"text": section.text, "section_type": section.section_type, "metadata": section.metadata, "embedding": vector}
            for section, vector in zip(sections, vectors)
        ],
    }


def embed_section_texts(texts: Iterable[str], api_key: Optional[str] = None, model: Optional[str] = None, api_base: Optional[str] = None, timeout: Optional[float] = None) -> Dict[str, Any]:
    client = create_embedding_client(api_key=api_key, model=model, api_base=api_base, timeout=timeout)
    normalized = [str(text).strip() for text in texts]
    vectors = client.embed_texts(normalized)
    return {"model": client.config.model, "embeddings": [{"text": text, "embedding": vector} for text, vector in zip(normalized, vectors)]}
