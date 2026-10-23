from amazon_translate import client

def local_request(text, source_lang, target_lang):
    translate_client = client.TranslateClient()
    response = translate_client.translate_text(Text=text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
    return response

def local_response(response):
    return response['TranslatedText']

def normalize_text(text):
    return text.strip().lower()