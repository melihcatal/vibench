import os
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version='2023-05-15',
    azure_endpoint=os.getenv('AZURE_OPENAI_ENDPOINT')
)

def answer_with_context(question, context):
    response = client.completions.create(
        model='text-davinci-003',
        prompt=f'Answer the following question using the provided context: {question}. Context: {context}',
        max_tokens=150
    )
    return response.choices[0].text.strip()