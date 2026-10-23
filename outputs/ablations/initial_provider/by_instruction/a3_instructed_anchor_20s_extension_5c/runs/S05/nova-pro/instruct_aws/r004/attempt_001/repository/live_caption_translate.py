import boto3

def live_caption_translate(caption, target_language):
    translate = boto3.client('translate')
    response = translate.translate_text(Text=caption, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return response['TranslatedText']