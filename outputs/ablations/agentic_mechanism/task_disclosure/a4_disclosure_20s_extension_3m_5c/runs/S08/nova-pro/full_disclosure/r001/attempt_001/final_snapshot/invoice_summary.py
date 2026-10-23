import os
import boto3

from botocore.exceptions import NoCredentialsError, PartialCredentialsError


def summarize_invoice_fields(invoice_fields):
    try:
        bedrock = boto3.client('bedrock', region_name='us-east-1')
        response = bedrock.invoke_model(
            model_id='amazon.titan-text-express-v1',
            body={
                'inputText': str(invoice_fields),
                'textGenerationConfig': {
                    'maxTokenCount': 512,
                    'temperature': 0.5,
                    'topP': 0.9
                }
            }
        )
        summary = response['outputText']
        return summary
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f'AWS credentials error: {e}')
        return None
    except Exception as e:
        print(f'Error summarizing invoice fields: {e}')
        return None