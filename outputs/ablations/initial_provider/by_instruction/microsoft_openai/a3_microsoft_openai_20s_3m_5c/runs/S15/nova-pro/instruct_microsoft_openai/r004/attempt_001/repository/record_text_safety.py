import os
import openai

class RecordSafetyChecker:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def check_record(self, record):
        try:
            response = openai.Completion.create(
                engine='text-davinci-003',
                prompt=f'Check if the following document contains unsafe content: {record}',
                max_tokens=150
            )
            safety_check = response.choices[0].text.strip()
            print('Record checked for safety successfully')
            return safety_check
        except Exception as e:
            print(f'Error checking record for safety: {e}')
            return None

if __name__ == '__main__':
    checker = RecordSafetyChecker()
    record = 'This is a sample document content for safety check.'
    safety_check = checker.check_record(record)