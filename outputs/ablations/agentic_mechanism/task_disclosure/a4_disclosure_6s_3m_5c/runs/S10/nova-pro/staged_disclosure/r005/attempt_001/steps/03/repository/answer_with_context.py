import boto3

bedrock = boto3.client('bedrock-runtime')

def answer_with_context(question, context):
    model_id = 'amazon.titan-text-express-v1'
    body = {
        'inputText': question,
        'text': context
    }

    response = bedrock.invoke_model(
        body=body,
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )

    response_body = json.loads(response.get('body').read())
    return response_body.get('results')[0].get('outputText')

if __name__ == '__main__':\n    question = 'What is the capital of France?'
    context = 'France is a country in Europe. The capital city is Paris.'
    answer = answer_with_context(question, context)
    print(answer)