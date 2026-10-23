import os
from google.cloud import translate_v2 as translate
from model_models import TranslationRequest, TranslationResponse


def translate_text(request: TranslationRequest) -> TranslationResponse:
    """
    Translates generated model output using Google Cloud Translation.
    Requires GOOGLE_APPLICATION_CREDENTIALS to be set, usually pointing to a service account key file.
    """
    translate_client = translate.Client()

    try:
        result = translate_client.translate(
            request.text,
            target_language=request.target_language,
            source_language=request.source_language,
        )
        return TranslationResponse(translated_text=result["translatedText"])
    except Exception as e:
        print(f"Error translating text: {e}")
        return TranslationResponse(translated_text="")


if __name__ == "__main__":
    # Example usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    # For local testing, you might need to set it to the path of your service account key file:
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/service_account_key.json"

    # Define a TranslationRequest
    # translate_req = TranslationRequest(
    #     text="Hello world, how are you?",
    #     target_language="es"
    # )

    # Perform translation
    # translated_res = translate_text(translate_req)
    # print(f"Original: {translate_req.text}")
    # print(f"Translated (es): {translated_res.translated_text}")

    # translate_req_fr = TranslationRequest(
    #     text="This is a test.",
    #     target_language="fr"
    # )
    # translated_res_fr = translate_text(translate_req_fr)
    # print(f"Original: {translate_req_fr.text}")
    # print(f"Translated (fr): {translated_res_fr.translated_text}")
    pass
