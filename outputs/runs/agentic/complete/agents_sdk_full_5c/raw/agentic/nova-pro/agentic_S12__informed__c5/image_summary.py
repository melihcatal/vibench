from google.cloud import translate_v2 as translate

def summarize_image_analysis(analysis):
    translation_client = translate.Client()
    translation = translation_client.translate(' '.join(analysis), target_language='en')
    return translation['translatedText']