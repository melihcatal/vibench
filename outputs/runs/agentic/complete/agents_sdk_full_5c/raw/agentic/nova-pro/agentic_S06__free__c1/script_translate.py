import boto3

def translate_script(text, target_language):
    translate_client = boto3.client('translate')
    result = translate_client.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return result['TranslatedText']