import boto3

def onboarding_summary(user_id, summary):
    translate = boto3.client('translate')
    result = translate.translate_text(Text=summary, SourceLanguageCode='en', TargetLanguageCode='es')
    return result['TranslatedText']