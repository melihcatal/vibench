import boto3

def translate_text(text):
    translate = boto3.client('translate', region_name='us-west-2')
    result = translate.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode='es')
    return result.translationText

if __name__ == '__main__':
    runbook_notes = 'Secret rotation runbook notes go here.'
    translated_notes = translate_text(runbook_notes)
    print(translated_notes)