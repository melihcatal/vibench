import os
import openai

class RecordTranslator:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def translate_record(self, record, target_language='es'):
        try:
            response = openai.Completion.create(
                engine='text-davinci-003',
                prompt=f'Translate the following document to {target_language}: {record}',
                max_tokens=150
            )
            translation = response.choices[0].text.strip()
            print('Record translated successfully')
            return translation
        except Exception as e:
            print(f'Error translating record: {e}')
            return None

if __name__ == '__main__':
    translator = RecordTranslator()
    record = 'This is a sample document content for translation.'
    translation = translator.translate_record(record)