# [HELPER] translation_models.py
"""Local request, response, and normalization helpers for General Text Translation.
Defines data structures for request payloads, API responses, and common normalization utilities.
"

from __future__ import annotations
from typing import Any, Dict, List, Optional
import json

# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------

class TranslateRequest:
    """Payload for translating a single text unit.

    Attributes:
        text: The source string to translate.
        target_lang: Language code for target (e.g., 'es').
        source_lang: Optional source language code (default 'en').
        preserve_markup: If True, ask provider to keep HTML tags (if supported).
    """
    def __init__(
        self,
        text: str,
        target_lang: str,
        source_lang: Optional[str] = None,
        preserve_markup: bool = False,
    ) -> None:
        self.text = text
        self.target_lang = target_lang
        self.source_lang = source_lang if source_lang else "en"
        self.preserve_markup = preserve_markup

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to a dict suitable for provider SDKs.
        Provider-specific keys are added in translation_client wrapper.
        """
        payload = {
            "text": self.text,
            "target_lang": self.target_lang,
            "source_lang": self.source_lang,
        }
        if self.preserve_markup:
            payload["preserve_markup"] = True
        return payload

# ---------------------------------------------------------------------------
# Response model (generic) - mirrors what a provider usually returns
# ---------------------------------------------------------------------------

class TranslateResponse:
    """Normalized translation result.

    Attributes:
        translated_text: The translated string.
        raw_response: Raw dict from the provider (kept for debugging)."
    """
    def __init__(self, translated_text: str, raw_response: Dict[str, Any]) -> None:
        self.translated_text = translated_text
        self.raw_response = raw_response

    def __repr__(self) -> str:
        return f"TranslateResponse(text='{self.translated_text}', raw={self.raw_response})"

# ---------------------------------------------------------------------------
# Normalization utilities
# ---------------------------------------------------------------------------

def normalize_response(raw: Dict[str, Any], provider: str = "deepl") -> TranslateResponse:
    """Convert provider-specific raw payload into a generic TranslateResponse.

    Args:
        raw: The raw dict coming from the SDK provider.
        provider: Identifier {'deepl', 'google'} to know which fields to read.

    Returns:
        A TranslateResponse instance.
    """
    if provider == "deepl":
        return TranslateResponse(
            translated_text=raw["text"],
            raw_response=raw,
        )
    elif provider == "google":
        return TranslateResponse(
            translated_text=raw["translatedText"],
            raw_response=raw,
        )
    else:
        raise ValueError(f"Unsupported provider for normalization: {provider}")

# ---------------------------------------------------------------------------
# Example usage (when script is run directly)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse, json
    parser = argparse.ArgumentParser(description="Translate a JSON payload and print normalized response.")
    parser.add_argument("payload", type=json.loads, help="JSON dict representing TranslateRequest.")
    parser.add_argument("provider", choices=["deepl", "google"], help="Translation provider."
    )
    args = parser.parse_args()
    # Simulate calling translation_client.translate_text_provider
    from translation_client import translate_text_provider
    raw = translate_text_provider(args.payload["text"], args.payload["target_lang"],
                                    args.payload.get("source_lang","en"), args.provider)
    resp = normalize_response(raw, args.provider)
    print(json.dumps(resp.__dict__, indent=2))