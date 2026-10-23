import boto3
from typing import Any, Dict
from security_client import SecretClient

def get_embedding_vector(secret_id: str) -> Dict[str, Any]:
    """Obtain an embedding vector for a secret using Amazon Titan Embeddings via Bedrock.

    The function demonstrates a concrete Bedrock Runtime SDK call and returns a dict
    containing the embedding array under the key 'embedding'.
    """
    bedrock = boto3.client('bedrock-runtime', region_name=os.getenv('AWS_REGION', 'us-east-1'))
    request_body = {
        'prompt': json.loads(client.get_secret_value(SecretId=secret_id).get('SecretString', '{}')).get('notes', '')
    }
    response = bedrock.invoke_model(
        Body=json.dumps(request_body),
        ModelId='amazon.titan-text-express-v1'
    )
    result = json.loads(response['Body'].read())
    # Assume the service returns {'embedding': [0.1, 0.2, ...]}
    return {'embedding': result.get('embedding', [])}
