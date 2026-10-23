import deepl

def translate_consent_copy(auth_key, text):
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang="EN-US")
    return result.text

if __name__ == "__main__":
    auth_key = "YOUR_DEEPL_AUTH_KEY"
    consent_copy = "Identity provider consent copy to be translated."
    translated_copy = translate_consent_copy(auth_key, consent_copy)
    print(translated_copy)