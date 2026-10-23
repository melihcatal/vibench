from google.cloud import translate_v2 as translate


def summarize_onboarding_state(text):
    translate_client = translate.Client()
    result = translate_client.translate(text, target_language="en")
    return result["translatedText"]
