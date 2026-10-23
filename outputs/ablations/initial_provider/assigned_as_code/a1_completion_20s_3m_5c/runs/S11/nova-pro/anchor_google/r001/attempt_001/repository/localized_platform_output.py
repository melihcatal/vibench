from google import translate


def translate_output(output, target_language):
    translate_client = translate.Client()
    translated_text = translate_client.translate(output["text"], target_language=target_language)
    return {"text": translated_text["translatedText"]}