import openai

openai.api_key = 'OPENAI_API_KEY'

def answer_with_context(question, context):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=f'Context: {context}\nQuestion: {question}\nAnswer:',
        max_tokens=150
    )
    return response.choices[0].text.strip()