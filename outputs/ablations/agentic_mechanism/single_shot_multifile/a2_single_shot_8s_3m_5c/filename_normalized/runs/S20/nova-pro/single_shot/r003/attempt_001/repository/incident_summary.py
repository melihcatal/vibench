import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def summarize_logs(logs):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=f'Summarize the following logs: {logs}',
        max_tokens=150
    )
    return response.choices[0].text.strip()

logs = 'Error: Database connection failed. Error: User authentication failed.'
print(summarize_logs(logs))