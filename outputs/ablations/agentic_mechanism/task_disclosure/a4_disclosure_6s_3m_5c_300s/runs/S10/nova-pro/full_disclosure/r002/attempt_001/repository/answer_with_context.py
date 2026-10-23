import boto3

def answer_with_context(question, context):
    client = boto3.client('bedrock-runtime')
    response = client.invoke_model(
        model_id='amazon.bedrock.model',
        body={
            'prompt': f'{context} Answer the following question: {question}',
            'max_tokens': 150
        }
    )
    result = response['body'].read()
    return result.decode('utf-8')
