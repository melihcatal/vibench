import boto3
import os

client = boto3.client(
    "bedrock-runtime",
    region_name="us-west-2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def embed_log_message(text):
    response = client.invoke_model(
        modelId="amazon.titan-embed-text-v1", body=json.dumps({"inputText": text})
    )
    result = json.loads(response["body"].read())
    return result["embedding"]


text = "This is a log message"
embedding = embed_log_message(text)
print(embedding)
