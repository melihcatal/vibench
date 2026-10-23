# appeal_translate.py
# [LATER-STEP] Translate appeal text for review

# Provider selection – we illustrate using DeepL for translation
PROVIDER = "deepl"


# -----------------------------------------------------------------------------
# Public API: translate an appeal description into the language required by reviewers
# -----------------------------------------------------------------------------
def translate_appeal(text: str, target_lang: str = "EN") -> str:
    """Translate appeal text using a concrete translation service.

    Args:
        text: The original appeal submitted by a user.
        target_lang: Language code for the translation destination (e.g., 'EN', 'FR').

    Returns:
        str: The translated appeal text ready for reviewer consumption.
    """
    if PROVIDER == "deepl":
        from deepl import Translator

        translator = Translator(auth_key=os.getenv("DEEPL_AUTH_KEY"))
        result = translator.translate_text(text, target_lang=target_lang.upper())
        return result.text
    elif PROVIDER == "google":
        from google.cloud import translate_v2 as translate

        client = translate.Client()
        result = client.translate(text, target_language=target_lang)
        return result["translatedText"]
    else:
        raise ValueError(f"Unsupported translation provider: {PROVIDER}")


# Example (would live in a driver script):
# appeal = "Je ne comprends pas pourquoi mon commentaire a été supprimé."
# print(translate_appeal(appeal, target_lang="EN"))
