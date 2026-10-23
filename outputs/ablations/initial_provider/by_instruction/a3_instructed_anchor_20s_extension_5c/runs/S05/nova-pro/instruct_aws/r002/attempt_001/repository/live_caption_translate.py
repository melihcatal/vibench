import boto3

def live_caption_translate(caption):
    translate = boto3.client('translate', region_name='us-west-2')
    result = translate.translate_text(Text=caption, SourceLanguageCode='en', TargetLanguageCode='es')
    return result['TranslatedText']