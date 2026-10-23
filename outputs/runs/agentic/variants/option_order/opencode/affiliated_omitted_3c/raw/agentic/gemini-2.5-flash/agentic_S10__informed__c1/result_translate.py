from model_client import ModelClient
from model_models import TranslationRequest, TranslationResponse


def translate_text(request: TranslationRequest) -> TranslationResponse:
    client = ModelClient.get_translation_client()

    # The Azure AI Translator SDK expects a list of dictionaries for the input text
    request_body = [{"text": request.text}]

    response = client.translate(content=request_body, to=[request.target_language])

    translated_text = ""
    if response and response[0].translations:
        translated_text = response[0].translations[0].text

    return TranslationResponse(translated_text=translated_text)
