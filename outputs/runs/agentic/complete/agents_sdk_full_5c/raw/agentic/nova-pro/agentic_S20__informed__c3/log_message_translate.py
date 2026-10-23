from google.cloud import translate

client = translate.TranslationServiceClient()

location = 'global'
target_language_code = 'es'

text = 'log message to translate'

response = client.translate_text(request={'parent': f'projects/-/locations/{location}', 'contents': [text], 'mime_type': 'text/plain', 'target_language_code': target_language_code})