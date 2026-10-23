import os
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Set up client
apikey = os.getenv("IBM_WATSON_APIKEY")
url = os.getenv("IBM_WATSON_URL")
authenticator = IAMAuthenticator(apikey)
language_translator = LanguageTranslatorV3(
    version="2018-05-01", authenticator=authenticator
)
language_translator.set_service_url(url)


# Moderate transcript text before publishing
def moderate_transcript(transcript):
    result = language_translator.identify(transcript).get_result()
    return result


if __name__ == "__main__":
    transcript = "This is a sample transcript."
    print(moderate_transcript(transcript))
