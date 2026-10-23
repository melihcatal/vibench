def translate_consent(copy):
    translated_copy = {}
    for key, value in copy.items():
        translated_copy[key] = f"Translated: {value}"
    return translated_copy