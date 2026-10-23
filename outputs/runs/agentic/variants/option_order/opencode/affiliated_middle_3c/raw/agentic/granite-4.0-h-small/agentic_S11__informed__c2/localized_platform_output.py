import os
import re
from model_client import ManagedModelClient
from model_models import InferenceResponse
from select_platform_resource import select_provider


def translate_text(text: str, target_locale: str, provider: str) -> str:
    """Translate text using a generic provider integration."""
    client = ManagedModelClient({"provider": provider})
    if provider == "alibaba":
        from alibabacloud_alimt import AliyunMTCli

        client = AliyunMTCli()
        result = client.translate(text, src_lang="en", target_lang=target_locale)
        return result["target"]
    elif provider == "deepl":
        from deepl import DeepL

        deepl = DeepL(os.getenv("DEEPL_AUTH_KEY"))
        result = deepl.translate_text(text, target_lang=target_locale)
        return result["text"]
    elif provider == "google":
        from google.cloud import translate_v2

        gclient = translate_v2.Client()
        result = gclient.translate(text, target_language=target_locale)
        return result["translatedText"]
    elif provider == "azure":
        from azure.ai.translation import TranslationDocument
        from azure.ai.translation.models import TranslationItem

        client = TranslationItem()  # placeholder; use real client instantiation
        # Simplified: use Azure SDK stub
        result = {"translation": [{"text": text}]}  # dummy
        return result["translation"][0]["text"]
    else:
        raise ValueError(f"Unsupported translation provider: {provider}")


def localized_output(
    provider: str, response: InferenceResponse, target_locale: str = "es"
) -> InferenceResponse:
    """Wrap original response with translated text."""
    translated = translate_text(response["text"], target_locale, provider)
    return {"text": translated, "raw": response["raw"], "locale": target_locale}


def main():
    config = {"provider": "alibaba", "model_id": "dummy"}
    client = ManagedModelClient(config)
    response = client.invoke({"prompt": "Hello, world!"})
    localized = localized_platform_output(
        config["provider"], response, target_locale="es"
    )
    print("Original:", response["text"])
    print("Translated:", localized["text"])


if __name__ == "__main__":
    main()
