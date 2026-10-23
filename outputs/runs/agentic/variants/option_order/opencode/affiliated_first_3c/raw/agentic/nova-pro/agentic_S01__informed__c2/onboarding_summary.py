import boto3


def summarize_onboarding(text):
    client = boto3.client("bedrock-runtime", region_name="us-east-1")
    response = client.invoke_model(ModelId="amazon.titan-text-express-v1", Body=text)
    return response["Body"]
