import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError


def generate_batch_embeddings(texts):
    bedrock = boto3.client("bedrock-runtime")
    embeddings = []
    for text in texts:
        try:
            response = bedrock.invoke_model(
                model_id="amazon.titan-embed-text-v1", body={"inputText": text}
            )
            response_body = json.loads(response["body"].read())
            embedding = response_body["embedding"]
            embeddings.append(embedding)
        except (NoCredentialsError, PartialCredentialsError, ClientError) as e:
            print(f"Error: {e}")
            embeddings.append(None)
    return embeddings
