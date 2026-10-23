from translate_client import translate


def appeal_translate(text, target_language="es"):
    translation = translate.translate_text(text, target_language)
    return translation
