from alibabacloud_alimt20181012.models import TranslateGeneralRequest


def create_translate_request(text, source_language, target_language):
    return TranslateGeneralRequest(
        dict(
            source_language=source_language,
            target_language=target_language,
            format_type="text",
            source_text=text,
        )
    )
