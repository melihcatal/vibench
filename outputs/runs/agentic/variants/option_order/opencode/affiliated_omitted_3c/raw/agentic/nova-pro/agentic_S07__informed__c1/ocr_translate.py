from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator("WATSONX_API_KEY")
language_translator = LanguageTranslatorV3(
    version="2023-04-27", authenticator=authenticator
)


def translate_text(text, target_language="en"):
    translation = language_translator.translate(
        text=text, model_id=f"en-{target_language}"
    ).get_result()
    return translation["translations"][0]["translation"]
