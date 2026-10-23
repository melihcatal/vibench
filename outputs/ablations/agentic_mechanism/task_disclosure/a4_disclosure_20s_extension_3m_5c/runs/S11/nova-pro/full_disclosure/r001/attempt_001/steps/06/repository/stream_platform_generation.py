import boto3

def stream_platform_generation(model_id, input_text):
    bedrock = boto3.client('bedrock-runtime')

    response = bedrock.invoke_model(
        modelId=model_id,
        body={
            'inputText': input_text
        }
    )

    for event in response['body']:
        yield event

if __name__ == '__main__':
    model_id = 'amazon.bedrock.model'
    input_text = 'Hello, world!'
    for event in stream_platform_generation(model_id, input_text):
        print(event)