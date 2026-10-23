import boto3


def summarize_onboarding_state(user_id):
    bedrock_client = boto3.client("bedrock-runtime")
    response = bedrock_client.invoke_model(
        ModelId="amazon.titan-text-express-v1",
        Body={"inputText": f"Summarize the onboarding state for user {user_id}"},
    )
    return response["body"]["text"]
