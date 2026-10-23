import os
import boto3

bedrock = boto3.client("bedrock-runtime", region_name="us-west-2")


def summarize_logs(logs):
    response = bedrock.invoke_model(
        model_id="amazon.titan-text-lite-v1", body={"inputText": logs}
    )
    return response["outputText"]
