import boto3


def log_embedding(text):
    bedrock = boto3.client("bedrock-runtime")
    response = bedrock.invoke_model(ModelId="amazon.titan-embed-text-v1", Body=text)
    print(response["Embedding"])
    print(f"Embedded log message")
