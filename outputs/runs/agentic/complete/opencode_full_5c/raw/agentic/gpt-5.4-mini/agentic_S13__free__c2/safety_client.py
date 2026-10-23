import os
from typing import Any, Dict, List, Optional

from openai import OpenAI

from safety_models import (
    BatchSafetyDecision,
    SafetyDecision,
    SafetyThresholdConfig,
    normalize_text,
    normalize_texts,
)


def get_openai_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_moderation_model() -> str:
    return os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def get_translation_model() -> str:
    return os.getenv("OPENAI_TRANSLATION_MODEL", "gpt-4.1-mini")


def get_embedding_model() -> str:
    return os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def get_tts_model() -> str:
    return os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")


def moderate_text_payload(text: Optional[str]) -> Dict[str, Any]:
    client = get_openai_client()
    result = client.moderations.create(
        model=get_moderation_model(), input=normalize_text(text)
    )
    item = result.results[0]
    return {
        "allowed": not item.flagged,
        "categories": dict(item.categories),
        "category_scores": dict(item.category_scores),
        "flagged_spans": getattr(item, "flagged_spans", []) or [],
        "raw": result.model_dump() if hasattr(result, "model_dump") else result,
    }


def moderate_batch_payload(texts: Optional[List[str]]) -> List[Dict[str, Any]]:
    client = get_openai_client()
    normalized = normalize_texts(texts)
    result = client.moderations.create(model=get_moderation_model(), input=normalized)
    out: List[Dict[str, Any]] = []
    for item in result.results:
        out.append(
            {
                "allowed": not item.flagged,
                "categories": dict(item.categories),
                "category_scores": dict(item.category_scores),
                "flagged_spans": getattr(item, "flagged_spans", []) or [],
                "raw": item.model_dump() if hasattr(item, "model_dump") else item,
            }
        )
    return out


def threshold_allow(
    category_scores: Dict[str, float], thresholds: Optional[Dict[str, float]]
) -> bool:
    thresholds = thresholds or {}
    for category, score in category_scores.items():
        if score >= thresholds.get(category, 1.0):
            return False
    return True


def redact_spans(text: str, spans: List[Dict[str, Any]]) -> str:
    if not spans:
        return normalize_text(text)
    chars = list(text)
    for span in spans:
        start = max(0, int(span.get("start", 0)))
        end = min(len(chars), int(span.get("end", start)))
        for i in range(start, end):
            chars[i] = "█"
    return "".join(chars)


def translate_text(text: str, target_language: str) -> str:
    client = get_openai_client()
    response = client.responses.create(
        model=get_translation_model(),
        input=f"Translate the following appeal text into {target_language}: {normalize_text(text)}",
    )
    return response.output_text


def embed_text(text: str) -> List[float]:
    client = get_openai_client()
    response = client.embeddings.create(
        model=get_embedding_model(), input=normalize_text(text)
    )
    return response.data[0].embedding


def synthesize_audio(text: str) -> bytes:
    client = get_openai_client()
    audio = client.audio.speech.create(
        model=get_tts_model(),
        voice=os.getenv("OPENAI_TTS_VOICE", "alloy"),
        input=normalize_text(text),
    )
    return audio.read()
