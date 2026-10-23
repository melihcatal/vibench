import boto3

bedrock = boto3.client(service_name='bedrock', region_name='us-east-1')

def generate_embedding(text):
    modelId = 'amazon.titan-text-embed-v1'
    accept = 'application/json'
    contentType = 'application/json'

    body = {
        'inputText': text
    }

    response = bedrock.invoke_model(body=json.dumps(body), modelId=modelId, accept=accept, contentType=contentType)
    response_body = json.loads(response.get('body').read())

    embedding = response_body.get('embedding')
    return embedding

# Example usage
metadata = 'Example metadata'
text = 'Example extracted text'

metadata_embedding = generate_embedding(metadata)
text_embedding = generate_embedding(text)

print('Metadata Embedding:', metadata_embedding)
print('Text Embedding:', text_embedding)