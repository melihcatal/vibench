from deepl import Translator


def welcome_translate(text: str, target_locale: str):
    translator = Translator(auth_key=__import__("os").environ["DEEPL_AUTH_KEY"])
    return translator.translate_text(
        text, target_lang=target_locale.split("-")[0].upper()
    ).text
