from google.cloud import translate_v2 as translate


def onboarding_summary(text):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language="en")
    return result["translatedText"]
