import os
from google.cloud import translate_v2 as translate
from identity_models import WelcomeMessageTranslateRequest, WelcomeMessageTranslateResponse

# Google Cloud Project ID
GOOGLE_CLOUD_PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")

def welcome_translate(request: WelcomeMessageTranslateRequest) -> WelcomeMessageTranslateResponse:
    if not GOOGLE_CLOUD_PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable is not set.")

    translate_client = translate.Client(project=GOOGLE_CLOUD_PROJECT_ID)

    try:
        result = translate_client.translate(
            request.text,
            target_language=request.target_language_code,
            source_language=request.source_language_code
        )
        return WelcomeMessageTranslateResponse(
            translated_text=result["translatedText"],
            detected_source_language=result.get("detectedSourceLanguage", request.source_language_code or "unknown")
        )
    except Exception as e:
        raise RuntimeError(f"Failed to translate welcome message: {e}")

if __name__ == '__main__':
    # This block is for demonstration/testing only
    # os.environ["GOOGLE_CLOUD_PROJECT_ID"] = "your-gcp-project-id"
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/gcp-service-account.json"
    # try:
    #     translate_req = WelcomeMessageTranslateRequest(
    #         text="Welcome to our service! We are happy to have you.",
    #         target_language_code="es"
    #     )
    #     translate_res = welcome_translate(translate_req)
    #     print(f"Original: '{translate_req.text}'")
    #     print(f"Translated ({translate_res.detected_source_language} -> {translate_req.target_language_code}): '{translate_res.translated_text}'")
    # except RuntimeError as e:
    #     print(f"Translation error: {e}")
    pass
