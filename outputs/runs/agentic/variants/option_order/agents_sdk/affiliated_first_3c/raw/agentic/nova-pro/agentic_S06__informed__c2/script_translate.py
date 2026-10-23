import boto3

def translate_script(text, source_language, target_language):
    translate_client = boto3.client('translate')
    result = translate_client.translate_text(Text=text, SourceLanguageCode=source_language, TargetLanguageCode=target_language)
    return result['TranslatedText']