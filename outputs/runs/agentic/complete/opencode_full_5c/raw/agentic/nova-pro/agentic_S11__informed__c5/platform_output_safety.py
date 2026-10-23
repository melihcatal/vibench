from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def check_safety(text):
    authenticator = IAMAuthenticator(os.getenv("WATSONX_API_KEY"))
    service = LanguageTranslatorV3(version="2018-05-01", authenticator=authenticator)
    service.set_service_url(os.getenv("WATSONX_URL"))
    translation = service.translate(text=text, model_id="en-fr").get_result()
    return translation["translations"][0]["translation"]
