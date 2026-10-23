import boto3

bedrock = boto3.client(service_name='bedrock', region_name='us-east-1')

def answer_with_context(question, context):
    prompt = f"Answer the following question using the provided context: {question}\nContext: {context}"
    response = bedrock.invoke_model(
        model_id='amazon.titan-text-express-v1',
        body={
            'prompt': prompt,
            'max_tokens': 200
        }
    )
    return response['body']['outputs'][0]['text']

if __name__ == '__main__':
    question = 'What is the capital of France?'
    context = 'France is a country in Europe.'
    answer = answer_with_context(question, context)
    print(answer)