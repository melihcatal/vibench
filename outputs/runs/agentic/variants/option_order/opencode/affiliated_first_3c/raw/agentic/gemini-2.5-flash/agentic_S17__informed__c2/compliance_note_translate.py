from security_client import SecurityClient
from security_models import TranslationRequest, TranslationResponse
import os


def translate_compliance_note(request: TranslationRequest) -> TranslationResponse:
    """Translates encryption or compliance notes for reviewers using Google Gemini API."""
    client = SecurityClient()

    if not client.gemini_model:
        return TranslationResponse(
            translated_text="Gemini API not configured. Please set GOOGLE_API_KEY."
        )

    # Google Gemini API: service=Google Gemini API; sdk=google-genai; interface=sdk; auth=GOOGLE_API_KEY
    prompt = f"Translate the following text into {request.target_language}:\n\n{request.text}\n\nTranslated text:"

    response = client.gemini_model.generate_content(
        prompt,
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        },
    )

    translated_text = response.text
    return TranslationResponse(translated_text=translated_text)
