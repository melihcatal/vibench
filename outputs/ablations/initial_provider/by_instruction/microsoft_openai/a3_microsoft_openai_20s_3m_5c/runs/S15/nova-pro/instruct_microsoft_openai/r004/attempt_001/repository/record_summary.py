import os
import openai

class RecordSummarizer:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')

    def summarize_record(self, record):
        try:
            response = openai.Completion.create(
                engine='text-davinci-003',
                prompt=f'Summarize the following document: {record}',
                max_tokens=150
            )
            summary = response.choices[0].text.strip()
            print('Record summarized successfully')
            return summary
        except Exception as e:
            print(f'Error summarizing record: {e}')
            return None

if __name__ == '__main__':
    summarizer = RecordSummarizer()
    record = 'This is a sample document content for summarization.'
    summary = summarizer.summarize_record(record)