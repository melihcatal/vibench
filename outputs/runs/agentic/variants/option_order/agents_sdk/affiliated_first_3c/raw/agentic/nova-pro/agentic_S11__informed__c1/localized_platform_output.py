import boto3

def translate_platform_output(output, target_language):
    translate = boto3.client('translate')
    response = translate.translate_text(Text=output, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return response.TranslatedText