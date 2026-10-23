from ibm_watson import LanguageTranslatorV3


def moderate_transcript(transcript):
    language_translator = LanguageTranslatorV3(
        version="2023-04-28",
        iam_apikey=os.getenv("IBM_STT_APIKEY"),
        url=os.getenv("IBM_STT_URL"),
    )
    result = language_translator.identify(text=transcript).get_result()
    return result
