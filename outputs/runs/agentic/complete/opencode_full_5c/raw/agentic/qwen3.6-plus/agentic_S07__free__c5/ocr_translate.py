from typing import Optional, List
from google.cloud import translate_v2 as translate
from google.api_core.client_options import ClientOptions
from document_models import TranslationRequest, TranslationResponse


GOOGLE_TRANSLATE_API_ENDPOINT = "translation.googleapis.com"
GOOGLE_TRANSLATE_MODEL = "nmt"


def translate_ocr_text(
    text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
    format: str = "text",
) -> TranslationResponse:
    client_options = ClientOptions(api_endpoint=GOOGLE_TRANSLATE_API_ENDPOINT)
    client = translate.Client(client_options=client_options)
    params = {"target": target_language, "format": format}
    if source_language:
        params["source"] = source_language
    result = client.translate(text, **params)
    translated_text = result.get("translatedText", "")
    detected_source = result.get("detectedSourceLanguage", source_language)
    return TranslationResponse(
        translated_text=translated_text,
        detected_source_language=detected_source,
        raw_response=result,
    )


def translate_ocr_text_batch(
    texts: List[str],
    target_language: str = "en",
    source_language: Optional[str] = None,
    format: str = "text",
) -> List[TranslationResponse]:
    client_options = ClientOptions(api_endpoint=GOOGLE_TRANSLATE_API_ENDPOINT)
    client = translate.Client(client_options=client_options)
    params = {"target": target_language, "format": format}
    if source_language:
        params["source"] = source_language
    results = client.translate(texts, **params)
    responses = []
    for result in results:
        translated_text = result.get("translatedText", "")
        detected_source = result.get("detectedSourceLanguage", source_language)
        responses.append(
            TranslationResponse(
                translated_text=translated_text,
                detected_source_language=detected_source,
                raw_response=result,
            )
        )
    return responses


def detect_language(text: str) -> str:
    client_options = ClientOptions(api_endpoint=GOOGLE_TRANSLATE_API_ENDPOINT)
    client = translate.Client(client_options=client_options)
    result = client.detect_language(text)
    if isinstance(result, list) and len(result) > 0:
        return result[0].get("language", "unknown")
    return result.get("language", "unknown")


def translate_with_glossary(
    text: str,
    target_language: str = "en",
    source_language: Optional[str] = None,
    glossary_name: Optional[str] = None,
) -> TranslationResponse:
    from google.cloud import translate_v3

    client = translate_v3.TranslationServiceClient()
    parent = "projects/{}/locations/global".format(
        __import__("os").environ.get("GOOGLE_CLOUD_PROJECT_ID", "")
    )
    contents = [text]
    request = translate_v3.TranslateTextRequest(
        contents=contents,
        target_language_code=target_language,
        parent=parent,
    )
    if source_language:
        request.source_language_code = source_language
    if glossary_name:
        glossary_config = translate_v3.TranslateTextGlossaryConfig(
            glossary=glossary_name, ignore_case=True
        )
        request.glossary_config = glossary_config
    response = client.translate_text(request=request)
    translated_text = (
        response.glossary_translations[0].translated_text
        if response.glossary_translations
        else response.translations[0].translated_text
    )
    return TranslationResponse(
        translated_text=translated_text,
        detected_source_language=source_language,
        raw_response={
            "translations": [t.translated_text for t in response.translations]
        },
    )
