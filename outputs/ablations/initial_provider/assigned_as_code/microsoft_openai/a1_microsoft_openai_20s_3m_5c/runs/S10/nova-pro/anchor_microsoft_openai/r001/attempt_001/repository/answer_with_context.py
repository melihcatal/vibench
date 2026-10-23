from.model_client import get_client

def answer_with_context(payload, config=None):
    client = get_client(config)
    response = client.chat.completions.create(model='gpt-5.4-mini',
        messages=[{'role': 'user', 'content': 'Answer the following question using the provided context:

Question: ' + payload['question'] + '

Context: ' + payload['context']}])
    return {'answer': response.choices[0].message.content or ''}