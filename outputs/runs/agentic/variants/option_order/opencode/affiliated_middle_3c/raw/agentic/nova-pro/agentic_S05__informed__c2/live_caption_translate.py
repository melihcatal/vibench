import deepl

DEEPL_AUTH_KEY = "your-deepl-auth-key"

client = deepl.Client(DEEPL_AUTH_KEY)


def live_caption_translate(text, target_lang="en"):
    result = client.translate_text(text, target_lang=target_lang)
    return result.text
