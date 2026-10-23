from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def secret_label_safety(text):
    authenticator = IAMAuthenticator(os.environ["WATSONX_API_KEY"])
    language_translator = LanguageTranslatorV3(
        version="2023-04-20", authenticator=authenticator
    )
    translation = language_translator.translate(
        text=text, model_id="en-es"
    ).get_result()
    return translation["translations"][0]["translation"]
