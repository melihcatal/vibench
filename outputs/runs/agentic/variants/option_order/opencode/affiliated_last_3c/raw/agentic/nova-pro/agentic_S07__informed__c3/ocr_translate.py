from deepl import Translator

# Initialize the client
translator = Translator(api_key=os.getenv("DEEPL_AUTH_KEY"))


def translate_text(text, target_lang="EN"):
    return translator.translate_text(text, target_lang=target_lang).text
