from identity_client import translate_client
from identity_models import TranslationRequest, normalize_locale


def translate_welcome(request: TranslationRequest):
    client = translate_client()
    target = normalize_locale(request.locale)
    response = client.translate_text(Text=request.text, SourceLanguageCode="en", TargetLanguageCode=target.split("-")[0])
    return {"translated_text": response.get("TranslatedText", ""), "target_locale": target}
