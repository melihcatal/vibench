import os
from google.cloud import translate_v2 as translate

translate_client = translate.Client(key=os.getenv('GOOGLE_APPLICATION_CREDENTIALS'))

result = translate_client.translate('Hello, world!', target_language='es')
print(result['translatedText'])