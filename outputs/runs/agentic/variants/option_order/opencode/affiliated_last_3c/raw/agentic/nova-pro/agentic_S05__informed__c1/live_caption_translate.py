from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Set up the Language Translator service
authenticator = IAMAuthenticator(os.getenv("IBM_TRANSLATOR_APIKEY"))
language_translator = LanguageTranslatorV3(
    version="2018-05-01", authenticator=authenticator
)
language_translator.set_service_url(os.getenv("IBM_TRANSLATOR_URL"))


def live_caption_translate(text, source_language="en", target_language="es"):
    translation = language_translator.translate(
        text=text, source=source_language, target=target_language
    ).get_result()
    return translation["translations"][0]["translation"]
