import os
from typing import Optional

import deepl

from storage_client import StorageClient


class DeepLTranslator:
    def __init__(self):
        self.auth_key = os.environ.get("DEEPL_AUTH_KEY")
        if not self.auth_key:
            raise ValueError(
                "DEEPL_AUTH_KEY environment variable is required for DeepL translation"
            )
        self.api_url = os.environ.get("DEEPL_API_URL")
        self._client = None

    @property
    def client(self) -> deepl.Translator:
        if self._client is None:
            kwargs = {"auth_key": self.auth_key}
            if self.api_url:
                kwargs["server_url"] = self.api_url
            self._client = deepl.Translator(**kwargs)
        return self._client

    def get_usage(self) -> dict:
        usage = self.client.get_usage()
        return {
            "character_count": usage.character.count,
            "character_limit": usage.character.limit,
        }

    def get_source_languages(self) -> list[dict]:
        return [
            {"code": lang.code, "name": lang.name}
            for lang in self.client.get_source_languages()
        ]

    def get_target_languages(self) -> list[dict]:
        return [
            {
                "code": lang.code,
                "name": lang.name,
                "supports_formality": lang.supports_formality,
            }
            for lang in self.client.get_target_languages()
        ]


def translate_stored_text(
    text: str,
    target_lang: str = "EN",
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
    preserve_formatting: bool = True,
    split_sentences: str = "on",
) -> dict:
    translator = DeepLTranslator()

    translate_kwargs = {
        "target_lang": target_lang,
        "preserve_formatting": preserve_formatting,
        "split_sentences": split_sentences,
    }

    if source_lang:
        translate_kwargs["source_lang"] = source_lang

    if formality:
        translate_kwargs["formality"] = formality

    result = translator.client.translate_text(text, **translate_kwargs)

    return {
        "translated_text": result.text,
        "detected_source_lang": result.detected_source_lang,
        "target_lang": target_lang,
        "source_lang": source_lang or result.detected_source_lang,
        "character_count": len(text),
    }


def translate_batch_stored_texts(
    texts: list[str],
    target_lang: str = "EN",
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
    preserve_formatting: bool = True,
    split_sentences: str = "on",
) -> list[dict]:
    translator = DeepLTranslator()

    translate_kwargs = {
        "target_lang": target_lang,
        "preserve_formatting": preserve_formatting,
        "split_sentences": split_sentences,
    }

    if source_lang:
        translate_kwargs["source_lang"] = source_lang

    if formality:
        translate_kwargs["formality"] = formality

    results = translator.client.translate_text(texts, **translate_kwargs)

    output = []
    for i, result in enumerate(results):
        output.append(
            {
                "original_text": texts[i],
                "translated_text": result.text,
                "detected_source_lang": result.detected_source_lang,
                "target_lang": target_lang,
                "character_count": len(texts[i]),
            }
        )

    return output


def translate_stored_document_text(
    bucket: Optional[str] = None,
    key: Optional[str] = None,
    target_lang: str = "EN",
    source_lang: Optional[str] = None,
    formality: Optional[str] = None,
) -> dict:
    storage_client = StorageClient()
    target_bucket = bucket or storage_client.default_bucket
    if not target_bucket:
        raise ValueError("No bucket specified and S3_DEFAULT_BUCKET not set")

    response = storage_client.s3_client.get_object(
        Bucket=target_bucket,
        Key=key,
    )

    content = response["Body"].read()
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        text = content.decode("latin-1")

    translation_result = translate_stored_text(
        text=text,
        target_lang=target_lang,
        source_lang=source_lang,
        formality=formality,
    )

    translation_result["bucket"] = target_bucket
    translation_result["key"] = key

    return translation_result
