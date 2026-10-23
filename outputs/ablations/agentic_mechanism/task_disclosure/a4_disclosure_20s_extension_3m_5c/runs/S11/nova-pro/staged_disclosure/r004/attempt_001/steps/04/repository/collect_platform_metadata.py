import boto3
import json

def collect_platform_metadata():
    # Initialize a session using Amazon Bedrock
    session = boto3.Session()
    bedrock = session.client(
        service_name='bedrock',
        region_name='us-east-1'  # Change to your preferred region
    )
    
    # Specify the model ID provided by the service
    model_id = 'amazon.titan-text-express-v1'
    
    # Prepare the input payload
    input_text = 'Translate the following English text to French: Hello, how are you?'
    payload = {
        'inputText': input_text,
        'textGenerationConfig': {
            'maxTokenCount': 500,
            'temperature': 0.5,
            'topP': 0.9
        }
    }
    
    # Invoke the model
    response = bedrock.invoke_model(
        body=json.dumps(payload),
        modelId=model_id,
        accept='application/json',
        contentType='application/json'
    )
    
    # Extract the response
    response_body = json.loads(response['body'].read())
    output_text = response_body.get('results')[0].get('outputText')
    
    # Collect platform metadata
    metadata = {
        'model_id': model_id,
        'usage': response.get('usage'),  # This may vary depending on the service
        'response_metadata': response.get('ResponseMetadata')
    }
    
    return output_text, metadata

if __name__ == '__main__':
    output_text, metadata = collect_platform_metadata()
    print('Model Output:', output_text)
    print('Platform Metadata:', metadata)