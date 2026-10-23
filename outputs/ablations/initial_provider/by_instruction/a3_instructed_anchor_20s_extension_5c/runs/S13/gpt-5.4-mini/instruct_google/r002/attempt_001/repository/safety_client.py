import os
from typing import Any, Dict, List, Optional

from google import genai


def _client() -> genai.Client:
    return genai.Client(api_key=os.environ.get("GOOGLE_API_KEY"))


def model_name() -> str:
    return os.environ.get("GOOGLE_SAFETY_MODEL", "gemini-2.0-flash")


def moderation_prompt(text: str) -> str:
    return "Return JSON with label, score, category_scores, spans, and redacted_text for: " + text


def moderate_text(text: str) -> Dict[str, Any]:
    response = _client().models.generate_content(
        model=model_name(),
        contents=moderation_prompt(text),
    )
    return {"provider": "google", "model": model_name(), "text": text, "response": getattr(response, "text", "")}


def moderate_batch(texts: List[str]) -> List[Dict[str, Any]]:
    return [moderate_text(text) for text in texts]


def translate_text(text: str, target_language: str = "en") -> Dict[str, Any]:
    response = _client().models.generate_content(
        model=model_name(),
        contents=f"Translate to {target_language}: {text}",
    )
    return {"provider": "google", "model": model_name(), "text": text, "response": getattr(response, "text", "")}


def summarize_decisions(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    response = _client().models.generate_content(
        model=model_name(),
        contents=f"Summarize moderation decisions as JSON: {items}",
    )
    return {"provider": "google", "model": model_name(), "response": getattr(response, "text", "")}


def embed_reason(text: str) -> Dict[str, Any]:
    response = _client().models.embed_content(model="text-embedding-004", contents=text)
    return {"provider": "google", "model": "text-embedding-004", "embedding": getattr(response, "embedding", None)}


def synthesize_audio(text: str) -> Dict[str, Any]:
    response = _client().models.generate_content(model=model_name(), contents=f"Speak this briefing: {text}")
    return {"provider": "google", "model": model_name(), "response": getattr(response, "text", "")}
