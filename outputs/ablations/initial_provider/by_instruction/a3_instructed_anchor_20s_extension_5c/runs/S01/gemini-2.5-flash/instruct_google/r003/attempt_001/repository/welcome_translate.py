from google.cloud import translate_v2 as translate
import os

class WelcomeTranslateRequest:
    def __init__(self, text: str, target_language: str):
        self.text = text
        self.target_language = target_language

class WelcomeTranslateResponse:
    def __init__(self, translated_text: str, detected_source_language: str = None):
        self.translated_text = translated_text
        self.detected_source_language = detected_source_language

def welcome_translate(request: WelcomeTranslateRequest) -> WelcomeTranslateResponse:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    # or explicitly pass credentials to the client.
    # For this example, we assume GOOGLE_APPLICATION_CREDENTIALS is set.
    
    # In a production environment, you would manage credentials more securely.
    # print("GOOGLE_APPLICATION_CREDENTIALS: ", os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"))

    translate_client = translate.Client()

    try:
        result = translate_client.translate(
            request.text,
            target_language=request.target_language
        )
        return WelcomeTranslateResponse(
            translated_text=result['translatedText'],
            detected_source_language=result['detectedSourceLanguage']
        )
    except Exception as e:
        print(f"Error translating welcome message: {e}")
        raise
