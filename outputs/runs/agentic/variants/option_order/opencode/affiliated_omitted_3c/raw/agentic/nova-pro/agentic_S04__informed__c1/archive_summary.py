import os
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


def archive_summary(text):
    authenticator = IAMAuthenticator(os.getenv("WATSONX_API_KEY"))
    language_translator = LanguageTranslatorV3(
        version="2018-05-01", authenticator=authenticator
    )
    summary = language_translator.summarize(text).get_result()
    return summary["summary"]
