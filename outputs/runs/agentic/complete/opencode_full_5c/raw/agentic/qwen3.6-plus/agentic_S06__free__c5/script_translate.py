from typing import List, Dict
from google.cloud import translate_v2 as translate


def translate_script(
    text: str,
    target_language: str,
    source_language: str = None,
    format_type: str = "text",
) -> str:
    client = translate.Client()
    params = {
        "q": text,
        "target": target_language,
        "format": format_type,
    }
    if source_language:
        params["source"] = source_language

    result = client.translate(**params)
    return result["translatedText"]


def translate_batch_scripts(
    texts: List[str], target_language: str, source_language: str = None
) -> List[Dict[str, str]]:
    client = translate.Client()
    results = client.translate(
        texts,
        target_language=target_language,
        source_language=source_language,
    )

    translated = []
    for i, result in enumerate(results):
        translated.append(
            {
                "original": texts[i],
                "translated": result["translatedText"],
                "detected_source": result.get(
                    "detectedSourceLanguage", source_language or "unknown"
                ),
                "target_language": target_language,
            }
        )
    return translated


def translate_with_glossary(
    text: str, target_language: str, glossary_terms: Dict[str, str] = None
) -> str:
    translated = translate_script(text, target_language)

    if glossary_terms:
        for source_term, target_term in glossary_terms.items():
            translated = translated.replace(source_term, target_term)

    return translated
