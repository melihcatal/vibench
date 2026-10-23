from observability_client import COMPREHEND

def translate_text(text, target_language):
    response = COMPREHEND.translate_text(Text=text, SourceLanguageCode='en', TargetLanguageCode=target_language)
    return response['TranslatedText']

text = 'This is a sample log message.'
translation = translate_text(text, 'es')
print(translation)