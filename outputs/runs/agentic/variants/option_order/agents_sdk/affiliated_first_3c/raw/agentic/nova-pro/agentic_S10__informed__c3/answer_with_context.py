import anthropic

def answer_with_context(question, context):
    client = anthropic.Client(api_key='ANTHROPIC_API_KEY')
    response = client.completions.create(
        model='claude-2.1',
        prompt=f'Answer the question based on the context below: {context}. Question: {question}',
        max_tokens_to_sample=1024
    )
    return response.completions[0].text