import boto3


def summarize_message_processing(results):
    bedrock_client = boto3.client("bedrock-runtime")
    response = bedrock_client.invoke_model(
        model_id="amazon.bedrock.model.v1", body=results
    )
    return response
