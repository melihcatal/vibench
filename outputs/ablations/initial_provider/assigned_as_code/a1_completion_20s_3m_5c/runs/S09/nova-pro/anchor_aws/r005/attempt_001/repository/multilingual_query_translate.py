import translate


def translate_query(query, target_language):
    translator = translate.Translator()
    translated_query = translator.translate(query, dest=target_language).text
    return translated_query