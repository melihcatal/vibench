import boto3

def answer_with_context(question, context):
    bedrock_client = boto3.client('bedrock-runtime')
    response = bedrock_client.invoke_model(
        model_id='amazon.bedrock.model',
        body={
            'prompt': f"Answer the following question using the provided context: {question}. Context: {context}",
            'max_tokens': 150
        }
    )
    result = response['body'].read()
    return result.decode('utf-8')