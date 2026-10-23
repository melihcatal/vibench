import boto3

def collect_metadata(model_id, input_text):
    bedrock = boto3.client('bedrock-runtime')
    response = bedrock.invoke_model(
        model_id=model_id,
        body={
            'inputText': input_text
        }
    )
    model_output = response['body'].read()
    metadata = {
        'usage': response['usage'],
        'model_id': model_id,
        'response_metadata': response['ResponseMetadata']
    }
    return model_output, metadata
