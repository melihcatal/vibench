from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator(os.getenv("WATSONX_API_KEY"))
language_translator = LanguageTranslatorV3(
    version="2018-05-01", authenticator=authenticator
)
language_translator.set_service_url(os.getenv("WATSONX_URL"))


def meeting_summary(transcript):
    response = language_translator.translate(
        text=transcript, model_id="en-es"
    ).get_result()
    return response["translations"][0]["translation"]
