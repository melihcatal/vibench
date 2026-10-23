import deepl


def batch_translate(texts, source_lang, target_lang):
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    results = translator.translate_text(
        texts, source_lang=source_lang, target_lang=target_lang
    )
    return [result.text for result in results]


if __name__ == "__main__":
    print(batch_translate(["Hello", "world"], "EN", "JA"))
