from safety_client import translate_text as google_translate_text


def appeal_translate(text, target_language="en"):
    return google_translate_text(text, target_language=target_language)
