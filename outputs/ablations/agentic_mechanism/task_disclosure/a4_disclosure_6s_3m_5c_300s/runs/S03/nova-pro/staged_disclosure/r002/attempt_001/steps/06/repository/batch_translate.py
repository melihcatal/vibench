import os
from google.cloud import translate_v2 as translate

def batch_translate(input_file, output_file, target_language):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/credentials.json'
    translator = translate.Client()

    with open(input_file, 'r') as f:
        texts = f.readlines()

    translations = translator.translate(texts, target_language=target_language)

    with open(output_file, 'w') as f:
        for translation in translations:
            f.write(translation['translatedText'] + '\n')

if __name__ == '__main__':
    batch_translate('input.txt', 'output.txt', 'es')