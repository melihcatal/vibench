import boto3


def translate_script(script, source_lang, target_lang):
    client = boto3.client('translate')
    response = client.translate_text(Text=script, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
    return response['TranslatedText']