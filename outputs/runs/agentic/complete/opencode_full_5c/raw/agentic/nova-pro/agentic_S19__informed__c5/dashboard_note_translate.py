import os

from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def dashboard_note_translate(text, target_language):
    authenticator = IAMAuthenticator(os.getenv("WATSONX_API_KEY"))
    language_translator = LanguageTranslatorV3(
        version="2023-04-01", authenticator=authenticator
    )
    response = language_translator.translate(
        text=text, model_id=f"en-{target_language}"
    ).get_result()
    return response
