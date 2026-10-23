import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError


def generate_embedding(text):
    bedrock = boto3.client("bedrock-runtime")
    try:
        response = bedrock.invoke_model(
            model_id="amazon.titan-embed-text-v1", body={"inputText": text}
        )
        response_body = json.loads(response["body"].read())
        embedding = response_body["embedding"]
        return embedding
    except (NoCredentialsError, PartialCredentialsError, ClientError) as e:
        print(f"Error: {e}")
        return None
