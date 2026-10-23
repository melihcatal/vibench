import os
from typing import Optional, Dict, Any, List

from identity_models import ConsentTranslation


DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"
DEEPL_API_URL_PRO = "https://api.deepl.com/v2/translate"
DEEPL_API_KEY = os.environ.get("DEEPL_API_KEY", "")


def translate_consent_text(
    text: str,
    target_lang: str,
    source_lang: Optional[str] = None,
    consent_type: str = "general",
    api_key: Optional[str] = None,
    use_pro: bool = False,
    provider_hint: Optional[str] = None,
) -> ConsentTranslation:
    import requests

    key = api_key or DEEPL_API_KEY
    base_url = DEEPL_API_URL_PRO if use_pro else DEEPL_API_URL

    params = {
        "text": text,
        "target_lang": target_lang.upper(),
        "auth_key": key,
    }
    if source_lang:
        params["source_lang"] = source_lang.upper()

    resp = requests.post(base_url, data=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    translated = data["translations"][0]["text"]
    detected_source = data["translations"][0].get(
        "detected_source_language", source_lang or "unknown"
    )

    return ConsentTranslation(
        source_language=detected_source.lower(),
        target_language=target_lang.lower(),
        original_text=text,
        translated_text=translated,
        consent_type=consent_type,
        provider=provider_hint or "deepl",
    )


def translate_consent_bundle(
    consent_texts: Dict[str, str],
    target_lang: str,
    source_lang: Optional[str] = None,
    api_key: Optional[str] = None,
    use_pro: bool = False,
) -> List[ConsentTranslation]:
    import requests

    key = api_key or DEEPL_API_KEY
    base_url = DEEPL_API_URL_PRO if use_pro else DEEPL_API_URL

    texts = list(consent_texts.values())
    params = {
        "text": texts,
        "target_lang": target_lang.upper(),
        "auth_key": key,
    }
    if source_lang:
        params["source_lang"] = source_lang.upper()

    resp = requests.post(base_url, data=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    results = []
    keys = list(consent_texts.keys())
    for i, translation in enumerate(data["translations"]):
        consent_type = keys[i] if i < len(keys) else "general"
        results.append(
            ConsentTranslation(
                source_language=translation.get(
                    "detected_source_language", source_lang or "unknown"
                ).lower(),
                target_language=target_lang.lower(),
                original_text=texts[i],
                translated_text=translation["text"],
                consent_type=consent_type,
                provider="deepl",
            )
        )

    return results


def translate_idp_consent_copy(
    idp_name: str,
    consent_copy: Dict[str, str],
    target_locales: List[str],
    api_key: Optional[str] = None,
    use_pro: bool = False,
) -> Dict[str, List[ConsentTranslation]]:
    translations_by_locale: Dict[str, List[ConsentTranslation]] = {}

    for locale in target_locales:
        translated = translate_consent_bundle(
            consent_texts=consent_copy,
            target_lang=locale,
            api_key=api_key,
            use_pro=use_pro,
        )
        translations_by_locale[locale] = translated

    return {
        "idp": idp_name,
        "translations": translations_by_locale,
        "provider": "deepl",
    }


def validate_consent_translation(
    original: str,
    translated: str,
    target_lang: str,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    import requests

    key = api_key or DEEPL_API_KEY
    base_url = DEEPL_API_URL_PRO if os.environ.get("DEEPL_USE_PRO") else DEEPL_API_URL

    resp = requests.post(
        base_url,
        data={
            "text": translated,
            "target_lang": "EN",
            "auth_key": key,
        },
        timeout=30,
    )
    resp.raise_for_status()
    back_translated = resp.json()["translations"][0]["text"]

    similarity = _compute_similarity(original.lower(), back_translated.lower())

    return {
        "original": original,
        "translated": translated,
        "back_translated": back_translated,
        "target_language": target_lang,
        "roundtrip_similarity": similarity,
        "provider": "deepl",
    }


def _compute_similarity(s1: str, s2: str) -> float:
    if not s1 or not s2:
        return 0.0
    words1 = set(s1.split())
    words2 = set(s2.split())
    if not words1 or not words2:
        return 0.0
    intersection = words1 & words2
    union = words1 | words2
    return len(intersection) / len(union)
