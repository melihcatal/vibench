import anthropic

anthropic.api_key = 'YOUR_ANTHROPIC_API_KEY'

def answer_with_context(question, context):
    response = anthropic.Completion.create(
        model='claude-2',
        prompt=f'Answer the following question using the provided context: {question}. Context: {context}',
        max_tokens_to_sample=100
    )
    return response.completion