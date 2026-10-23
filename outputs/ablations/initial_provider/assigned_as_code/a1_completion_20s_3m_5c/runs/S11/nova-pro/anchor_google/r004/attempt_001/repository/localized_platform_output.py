import os
from google.cloud import translate_v2 as translate

def localized_platform_output(output, target_language):
    translate_client = translate.Client()
    result = translate_client.translate(output, target_language=target_language)
    return result['translatedText']

model = select_platform_resource()
for output in stream_platform_generation(model):
    translated_output = localized_platform_output(output, 'es')
    print(translated_output)