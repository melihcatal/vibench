import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def summarize_records(records):
    try:
        bedrock_client = boto3.client('bedrock-runtime')
        response = bedrock_client.invoke_model(
            model_id='amazon.titan-text-express-v1',
            body={
                'inputText': '
'.join([str(record) for record in records]),
                'textSize': 'small'
            }
        )
        result = json.loads(response['body'].read())
        return result.get('summary', '')
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f'Error: {e}')
        return ''