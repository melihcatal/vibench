from translation_client import translate_dictionary_values_value


def translate_dictionary_values(payload: dict[str, str], target_language: str, source_language: str | None = None) -> dict[str, str]:
    return translate_dictionary_values_value(payload, target_language, source_language)
