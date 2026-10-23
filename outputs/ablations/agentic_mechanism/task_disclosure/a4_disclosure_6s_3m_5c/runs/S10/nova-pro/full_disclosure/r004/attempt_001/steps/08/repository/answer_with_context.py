import boto3

def answer_with_context(question, context):
    client = boto3.client('bedrock-runtime')
    prompt = f"Answer the following question using the provided context:\nQuestion: {question}\nContext: {context}"
    response = client.invoke_model(
        model_id='amazon.titan-text-express-v1',
        body={
            'inputText': prompt,
            'textGenerationConfig': {
                'maxTokenCount': 2048,
                'stopSequences': [],
                'temperature': 0.5,
                'topP': 0.9
            }
        }
    )
    result = response['body'].read()
    output = json.loads(result)['outputText']
    return output