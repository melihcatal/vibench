import os
from observability_client import get_generative_model_client
from observability_models import TranslationRequest, TranslationResponse


def translate_log_message(request: TranslationRequest) -> TranslationResponse:
    """
    Translates a log message to a specified locale for support teams
    using Google's Gemini model.
    """
    model = get_generative_model_client(model_name="gemini-1.5-flash-001")

    prompt = (
        f"Translate the following log message into the language corresponding "
        f"to the locale code '{request.target_locale}'. "
        f"Return only the translated text.\n\n"
        f'Log Message: "{request.text}"'
    )

    response = model.generate_content(prompt)

    translated_text = response.text.strip()
    return TranslationResponse(translated_text=translated_text)


if __name__ == "__main__":
    if os.environ.get("GCP_PROJECT_ID"):
        log_message = "User session timed out due to inactivity."

        # Example: Translate to French
        fr_request = TranslationRequest(text=log_message, target_locale="fr")
        fr_response = translate_log_message(fr_request)
        print(f"Original: {log_message}")
        print(f"French (fr): {fr_response.translated_text}")

        # Example: Translate to Spanish
        es_request = TranslationRequest(text=log_message, target_locale="es")
        es_response = translate_log_message(es_request)
        print(f"Spanish (es): {es_response.translated_text}")
    else:
        print("GCP_PROJECT_ID environment variable not set. Skipping example run.")
