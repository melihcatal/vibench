import boto3

def answer_with_context(question, context):
    bedrock = boto3.client('bedrock-runtime')
    response = bedrock.invoke_model(
        model_id='amazon.bedrock.model',
        body={
            'prompt': f'{context} {question}',
            'max_tokens': 150
        }
    )
    answer = response['output']['text']
    return answer