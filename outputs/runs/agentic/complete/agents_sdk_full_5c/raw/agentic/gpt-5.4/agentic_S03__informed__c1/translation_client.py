from __future__ import annotations

import os
from typing import Iterable, List, Optional

import deepl

from translation_models import TranslationResult

DEFAULT_DEEPL_MODEL_TYPE = "prefer_quality_optimized"


class DeepLTranslationClient:
    def __init__(
        self,
        auth_key: Optional[str] = None,
        server_url: Optional[str] = None,
        model_type: str = DEFAULT_DEEPL_MODEL_TYPE,
    ) -> None:
        api_key = auth_key or os.environ["DEEPL_AUTH_KEY"]
        self.translator = deepl.Translator(auth_key=api_key, server_url=server_url)
        self.model_type = model_type

    def translate_text(
        self,
        text: str,
        *,
        target_language: str,
        source_language: Optional[str] = None,
        tag_handling: Optional[str] = None,
        split_sentences: Optional[str] = None,
        preserve_formatting: bool = False,
        outline_detection: Optional[bool] = None,
        ignore_tags: Optional[Iterable[str]] = None,
    ) -> TranslationResult:
        response = self.translator.translate_text(
            text,
            target_lang=target_language.upper(),
            source_lang=source_language.upper() if source_language else None,
            tag_handling=tag_handling,
            split_sentences=split_sentences,
            preserve_formatting=preserve_formatting,
            outline_detection=outline_detection,
            ignore_tags=list(ignore_tags) if ignore_tags is not None else None,
            model_type=self.model_type,
        )
        billed = getattr(response, "billed_characters", None)
        return TranslationResult(
            text=response.text,
            detected_source_language=getattr(response, "detected_source_lang", None),
            billed_characters=billed,
            provider="DeepL",
            raw={
                "model_type": self.model_type,
                "detected_source_lang": getattr(response, "detected_source_lang", None),
                "billed_characters": billed,
            },
        )

    def translate_batch(
        self,
        texts: List[str],
        *,
        target_language: str,
        source_language: Optional[str] = None,
        preserve_formatting: bool = False,
    ) -> List[TranslationResult]:
        responses = self.translator.translate_text(
            texts,
            target_lang=target_language.upper(),
            source_lang=source_language.upper() if source_language else None,
            preserve_formatting=preserve_formatting,
            model_type=self.model_type,
        )
        return [
            TranslationResult(
                text=item.text,
                detected_source_language=getattr(item, "detected_source_lang", None),
                billed_characters=getattr(item, "billed_characters", None),
                provider="DeepL",
                raw={
                    "model_type": self.model_type,
                    "detected_source_lang": getattr(item, "detected_source_lang", None),
                    "billed_characters": getattr(item, "billed_characters", None),
                },
            )
            for item in responses
        ]


def get_translation_client() -> DeepLTranslationClient:
    return DeepLTranslationClient(
        auth_key=os.getenv("DEEPL_AUTH_KEY"),
        server_url=os.getenv("DEEPL_SERVER_URL"),
        model_type=os.getenv("DEEPL_MODEL_TYPE", DEFAULT_DEEPL_MODEL_TYPE),
    )
