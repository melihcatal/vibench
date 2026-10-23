from ibm_watson import LanguageTranslatorV3

def get_models():
    return LanguageTranslatorV3().list_models().get_result()