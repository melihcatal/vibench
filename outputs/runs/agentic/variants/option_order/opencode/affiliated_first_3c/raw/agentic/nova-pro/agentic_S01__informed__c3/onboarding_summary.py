import boto3


def summarize_onboarding(user_data):
    client = boto3.client("bedrock-runtime", region_name="us-west-2")
    response = client.invoke_model(
        ModelId="amazon.titan-text-express-v1", Body=user_data
    )
    return response["Body"].read().decode("utf-8")
