from google.cloud import translate_v2 as translate

def translate_output(output_text, target_language='es'):
    translate_client = translate.Client()
    translation = translate_client.translate(output_text, target_language=target_language)
    return translation['translatedText']