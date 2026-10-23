import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

logs = [
    'Error: Database connection failed',
    'Warning: User authentication failed'
]
summary = openai.Completion.create(
    engine='text-davinci-003',
    prompt=f'Summarize the following logs: {logs}',
    max_tokens=100
)
print(summary.choices[0].text)
