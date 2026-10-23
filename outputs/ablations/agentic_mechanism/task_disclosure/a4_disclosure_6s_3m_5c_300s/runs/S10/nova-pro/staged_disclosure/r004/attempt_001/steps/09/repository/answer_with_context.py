import boto3

bedrock = boto3.client(service_name='bedrock', region_name='us-east-1')

def answer_with_context(question, context):
    model_id = 'amazon.titan-text-express-v1'
    body = {
        'inputText': question,
        'text': context
    }
    response = bedrock.invoke_model(
        modelId=model_id,
        body=body
    )
    result = response['outputText']
    return result

if __name__ == '__main__':
    question = 'What is the capital of France?'
    context = 'France is a country in Europe. Its capital and largest city is Paris.'
    answer = answer_with_context(question, context)
    print(answer)