import boto3

def translate_script(script, target_language):
    translate_client = boto3.client('translate')
    result = translate_client.translate_text(Text=script, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return result['TranslatedText']