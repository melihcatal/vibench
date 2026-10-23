def normalize_translation_payload(text, source_language, target_language):
    return {
        "Text": text,
        "SourceLanguageCode": source_language,
        "TargetLanguageCode": target_language,
    }


def normalize_translation_response(response):
    return {
        "text": response["TranslatedText"],
        "source_language": response["SourceLanguageCode"],
        "target_language": response["TargetLanguageCode"],
    }