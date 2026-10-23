# dashboard_note_translate.py
# Translate metric or dashboard notes for another locale

from observability_client import ObservabilityClient
from observability_models import TranslationRequest, TranslationResponse
import os

def translate_note(service: str, text: str, target_locale: str) -> TranslationResponse:
    """Translate a dashboard or metric note into a target locale using a provider.
    Returns a TranslationResponse with the translated text."""
    client = ObservabilityClient.get_client(service)
    # Choose translation provider based on service/context
    if client["service"] in ("datadog", "google", "aws"):
        # Google Cloud Translation (fallback using env var)
        credentials = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if not credentials:
            raise RuntimeError("GOOGLE_APPLICATION_CREDENTIALS not set for translation")
        from google.cloud import translate_v2 as translate
        client_lib = translate.Client()
        result = client_lib.translate(text, target_language=target_locale)
        return TranslationResponse(translated_text=result["translatedText"])
    elif client["service"] == "aws":
        # Amazon Translate
        import boto3
        client_lib = boto3.client("translate", region_name="us-east-1")
        result = client_lib.TranslateText(Text=text, SourceLanguageCode="auto", TargetLanguageCode=target_locale)
        translated = result["TranslatedText"]
        return TranslationResponse(translated_text=translated)
    elif client["service"] == "alibaba":
        # Alibaba Cloud Translation
        import aliyun-python-sdk-core as core
        from aliyunsdkalimt.request.v20181012 import TranslateTextRequest
        client_lib = core.DefaultAcsClient(
            access_key_id=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID"),
            access_key_secret=os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
        )
        request = TranslateTextRequest.TranslateTextRequest()
        request.set_LanguageCode(target_locale)
        request.set_SourceLanguageCode("auto")
        request.set_Text(text)
        response = client_lib.get_response(request)
        # Assume JSON with field translated_text
        translated = response.get("translated_text", text)
        return TranslationResponse(translated_text=translated)
    else:
        raise ValueError(f"Unsupported service {service} for note translation")
