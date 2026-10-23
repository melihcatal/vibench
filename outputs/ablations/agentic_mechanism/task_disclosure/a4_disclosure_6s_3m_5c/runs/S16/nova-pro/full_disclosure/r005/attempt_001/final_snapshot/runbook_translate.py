import boto3

def translate_runbook_notes(runbook_notes):
    client = boto3.client('translate')
    result = client.translate_text(Text=runbook_notes, SourceLanguageCode='en', TargetLanguageCode='es')
    return result.get('TranslatedText', '')

if __name__ == '__main__':
    runbook_notes = 'Enter your runbook notes here.'
    translated_notes = translate_runbook_notes(runbook_notes)
    print(translated_notes)