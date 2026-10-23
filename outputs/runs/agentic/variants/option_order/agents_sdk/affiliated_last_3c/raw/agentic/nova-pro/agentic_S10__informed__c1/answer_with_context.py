import openai

openai.api_key = os.getenv('OPENAI_API_KEY')

def answer_with_context(question, context):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=f'Answer the following question using the provided context: {question}. Context: {context}',
        max_tokens=150
    )
    return response.choices[0].text.strip()