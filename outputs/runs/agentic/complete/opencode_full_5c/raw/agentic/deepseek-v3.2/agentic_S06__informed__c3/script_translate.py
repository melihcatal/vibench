import os
import deepl


def translate_text(text, target_lang="EN-US", source_lang=None):
    auth_key = os.environ.get("DEEPL_AUTH_KEY")

    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable must be set")

    translator = deepl.Translator(auth_key)

    try:
        if source_lang:
            result = translator.translate_text(
                text, target_lang=target_lang, source_lang=source_lang
            )
        else:
            result = translator.translate_text(text, target_lang=target_lang)

        return {
            "translated_text": result.text,
            "source_lang": result.detected_source_lang
            if hasattr(result, "detected_source_lang")
            else source_lang,
            "target_lang": target_lang,
        }
    except deepl.DeepLException as e:
        raise Exception(f"DeepL translation failed: {str(e)}")


def translate_narration_script(
    script_text, target_lang="EN-US", preserve_formatting=True
):
    auth_key = os.environ.get("DEEPL_AUTH_KEY")

    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable must be set")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(
            script_text,
            target_lang=target_lang,
            preserve_formatting=preserve_formatting,
        )

        return result.text
    except deepl.DeepLException as e:
        raise Exception(f"DeepL translation failed: {str(e)}")


def batch_translate_scripts(scripts, target_lang="EN-US"):
    auth_key = os.environ.get("DEEPL_AUTH_KEY")

    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable must be set")

    translator = deepl.Translator(auth_key)

    try:
        results = []
        for script in scripts:
            result = translator.translate_text(script, target_lang=target_lang)
            results.append(
                {
                    "original": script,
                    "translated": result.text,
                    "detected_lang": result.detected_source_lang
                    if hasattr(result, "detected_source_lang")
                    else None,
                }
            )

        return results
    except deepl.DeepLException as e:
        raise Exception(f"DeepL batch translation failed: {str(e)}")


def get_supported_languages():
    auth_key = os.environ.get("DEEPL_AUTH_KEY")

    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable must be set")

    translator = deepl.Translator(auth_key)

    try:
        source_langs = translator.get_source_languages()
        target_langs = translator.get_target_languages()

        return {
            "source_languages": [
                {"code": lang.code, "name": lang.name} for lang in source_langs
            ],
            "target_languages": [
                {"code": lang.code, "name": lang.name} for lang in target_langs
            ],
        }
    except deepl.DeepLException as e:
        raise Exception(f"Failed to get supported languages: {str(e)}")


def translate_with_glossary(text, target_lang="EN-US", glossary_id=None):
    auth_key = os.environ.get("DEEPL_AUTH_KEY")

    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable must be set")

    translator = deepl.Translator(auth_key)

    try:
        if glossary_id:
            result = translator.translate_text(
                text, target_lang=target_lang, glossary=glossary_id
            )
        else:
            result = translator.translate_text(text, target_lang=target_lang)

        return result.text
    except deepl.DeepLException as e:
        raise Exception(f"DeepL translation with glossary failed: {str(e)}")
