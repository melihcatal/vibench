import boto3

def translate_markup(text, source_language, target_language):
    client = boto3.client('translate')
    response = client.translate_text(
        Text=text,
        SourceLanguageCode=source_language,
        TargetLanguageCode=target_language,
        TerminologyNames=[]
    )
    return response['TranslatedText']

if __name__ == '__main__':
    sample_text = '<p>Hello, world!</p>'
    translated_text = translate_markup(sample_text, 'en', 'es')
    print(translated_text)