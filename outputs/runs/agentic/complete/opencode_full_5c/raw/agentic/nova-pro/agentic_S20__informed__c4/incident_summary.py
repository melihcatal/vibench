import boto3


def summarize_error_logs(log_events):
    client = boto3.client("bedrock-runtime", region_name="us-west-2")
    response = client.invoke_model(
        modelId="anthropic.claude-v2",
        body={
            "prompt": f"Summarize the following error logs: {log_events}",
            "max_tokens_to_sample": 1024,
        },
    )
    return response["body"]["summary"]
