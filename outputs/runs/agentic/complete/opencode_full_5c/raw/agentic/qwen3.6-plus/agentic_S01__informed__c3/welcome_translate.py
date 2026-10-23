import os
import deepl
from identity_models import TranslationRequest, TranslationResponse


DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")
DEEPL_API_URL = "https://api-free.deepl.com"


def translate_welcome_copy(
    text: str,
    target_lang: str,
    source_lang: str = None,
) -> TranslationResponse:
    translator = deepl.Translator(DEEPL_AUTH_KEY)

    request = TranslationRequest(
        text=text,
        target_lang=target_lang,
        source_lang=source_lang,
    )

    params = request.to_deepl_params()
    source_lang_param = params.pop("source_lang", None)
    text_to_translate = params.pop("text")
    target_lang_val = params.pop("target_lang")

    result = translator.translate_text(
        text_to_translate,
        target_lang=target_lang_val,
        source_lang=source_lang_param,
    )

    return TranslationResponse(
        translated_text=result.text,
        detected_source_lang=result.detected_source_lang,
        raw_response={
            "text": result.text,
            "detected_source_lang": result.detected_source_lang,
        },
    )


if __name__ == "__main__":
    result = translate_welcome_copy(
        text="Welcome to our platform! Let's get you started.",
        target_lang="ES",
    )
    print(result)
