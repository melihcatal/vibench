import os
import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def invoice_summary(invoice_data):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=f'Summarize the following invoice: {invoice_data}',
        max_tokens=100
    )
    return response.choices[0].text.strip()