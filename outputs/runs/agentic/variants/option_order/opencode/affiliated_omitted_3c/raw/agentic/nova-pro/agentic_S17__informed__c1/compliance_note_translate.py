import os
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def compliance_note_translate(api_key, url, text, target_language):
    authenticator = IAMAuthenticator(api_key)
    language_translator = LanguageTranslatorV3(
        version="2021-08-01", authenticator=authenticator
    )
    language_translator.set_service_url(url)
    translation = language_translator.translate(
        text=text, model_id=f"en-{target_language}"
    ).get_result()
    return translation["translations"][0]["translation"]
