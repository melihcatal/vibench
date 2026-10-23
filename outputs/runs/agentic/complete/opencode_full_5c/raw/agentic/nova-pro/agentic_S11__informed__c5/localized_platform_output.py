from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def translate_output(text, target_language="es"):
    authenticator = IAMAuthenticator(os.getenv("WATSONX_API_KEY"))
    service = LanguageTranslatorV3(version="2018-05-01", authenticator=authenticator)
    service.set_service_url(os.getenv("WATSONX_URL"))
    translation = service.translate(
        text=text, model_id="en-" + target_language
    ).get_result()
    return translation["translations"][0]["translation"]
