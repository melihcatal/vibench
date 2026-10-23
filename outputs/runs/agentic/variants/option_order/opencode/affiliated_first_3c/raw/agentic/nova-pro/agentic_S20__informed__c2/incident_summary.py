import boto3


def summarize_error_logs(log_group_name, query):
    client = boto3.client("bedrock-runtime")
    response = client.invoke_model(
        modelId="amazon.titan-text-express-v1", body={"inputText": query}
    )
    return response["outputText"]
