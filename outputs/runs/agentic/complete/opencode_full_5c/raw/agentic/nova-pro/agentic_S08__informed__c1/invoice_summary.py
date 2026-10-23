import os
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def invoice_summary(invoice):
    authenticator = IAMAuthenticator(os.getenv("WATSONX_API_KEY"))
    language_translator = LanguageTranslatorV3(
        version="2023-04-01", authenticator=authenticator
    )
    summary = language_translator.summarize(
        text=invoice["notes"], model_id="en"
    ).get_result()
    return summary["summary"]
